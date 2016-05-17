from django.shortcuts import render

# Create your views here.
import logging
import requests
import geocoder
import uuid
from datetime import datetime
from django.http import JsonResponse
from uber_pricing.models import RequestRecord
from twilio.rest import TwilioRestClient 

UBER_SERVER_TOKEN='IUjVXyf4Hu1ZkDgirOI9xJy-X9rCpwOvbwWsSpJy'
UBER_URL='https://api.uber.com/v1/estimates/price'
UBER_PRODUCT='uberX'

 
# put your own credentials here 
TWILIO_ACCOUNT_SID = "AC06e1e5044efc68a5ffd771cb7b15a9d7" 
TWILIO_AUTH_TOKEN = "03041fc0e3a2d1b485c41202cd6b03fb" 
TWILIO_PHONE_NUMBER = "+16697211250"



logger = logging.getLogger(__name__)

def validate_buy_params(request):
    try:
        phone_number = request.data['phone_number']
        len(phone_number) == 10
    except ValueError:
        logger.info('ValueError for buy params: {}'.format(request.data))
         raise ValidationError({"error_message": "Phone number must be 10 digits long"})
    try:
        current_address = request.data['current_address']
        geocoded.latlng = geocoder.google(current_address)
    except ValueError:
        logger.info('ValueError for buy params: {}'.format(request.data))
        raise ValidationError({"error_message": "Must submit valid address"})
    try:
        surge_threshold = request.data['surge_multiplier']
        surge_threshold >= 1
    except ValueError:
        logger.info('ValueError for buy params: {}'.format(request.data))
        raise ValidationError({"error_message": "Surge multiplier must be >= 1"})

    return phone_number, current_address, surge_threshold

def call_uber_api(current_address):
	LATITUDE, LONGITUDE = geocoder.google(current_address).latlng
	parameters = {
		'server_token':UBER_SERVER_TOKEN,
		'start_latitude':LATITUDE,
		'start_longitude':LONGITUDE,
		'end_latitude': LATITUDE +.01,
		'end_longitude': LONGITUDE +.01,
	}
	response = requests.get(UBER_URL, parameters)
	data = response.json()['prices']
	uberX_multiplier= [d['surge_multiplier'] for d in data if d['localized_display_name'] =='uberX'][0]
	return uberX_multiplier

def text_user(phone_number, current_surge_multiplier, surge_threshold):
	client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	formatted_number = "+1{}".format(str(phone_number)) 
 	client.messages.create(to=formatted_number, from_=TWILIO_PHONE_NUMBER,
 	body="This is an auto-generated from SurgeProtector! The current surge multiplier for uberX is {0} which is below your specified surge threshold of {1}. Have a nice day!".format(str(current_surge_multiplier), str(surge_threshold))) 

@api_view(['POST'])
@payment.required(get_price)
def buy_readings(request):
    try:
        phone_number, current_address, surge_threshold= validate_buy_params(request)
    except ValidationError as error:
        return JsonResponse(error.message_dict, status=400)
    current_surge_multiplier = call_uber_ai(current_address)
    if current_surge_multiplier <= surge_threshold:
    	text_user(phone_number, current_surge_multiplier, surge_threshold)
    	return JSonResponse({"message": "Thank you for your business! We will alert your phone when surge has dropped below your threshold. Have a nice day!", "current_surge_multiplier": current_surge_multiplier})
    current_request = RequestRecord(
    	unique_id = uuid.uuid4(),
    	last_time_checked = datetime.now(),
    	phone_number = phone_number,
    	last_surge_multiplier = current_surge_multiplier,
    	surge_threshold = surge_threshold,
    	contacted = False)
  	current_request.save()
  	return JSonResponse({"message": "Thank you for your business! We will alert your phone when surge has dropped below your threshold. Have a nice day!", "current_surge_multiplier": current_surge_multiplier})

if __name__=='__main__':
	





