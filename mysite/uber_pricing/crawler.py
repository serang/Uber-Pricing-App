from requests.exceptions import RequestException
from urllib.parse import urlparse
import sys
import queue
import threading
import logging

from datetime import datetime
from mkt import settings
from mkt.models import RequestRecords
from uber_pricing.views import call_uber_api, text_user
from twilio.rest import TwilioRestClient

UBER_SERVER_TOKEN=settings.UBER_SERVER_TOKEN
UBER_URL=settings.UBER_URL
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER



def process_task(request):
    new_surge_multiplier = call_uber_api(request.current_address)
    new_time_updated = datetime.now()
    if new_surge_multiplier <= request.surge_threshold:
        text_user(request.phone_number, new_surge_multiplier, request.surge_threshold)
        request.contacted = True
    request.update_or_create(
        last_time_checked=new_time_updated,
        phone_number = request.phone_number,
        last_surge_multiplier = new_surge_multiplier,
        surge_threshold = request.surge_threshold,
        contacted = request.contacted
        current_address = request.current_address)
    return

def do_work(work_queue):
    """
    Executes jobs from the work queue and updates respones and errors.
    """
    while not work_queue.empty():
        if work_queue.empty():
            return
        task = work_queue.get()
        process_task(task)
    return


def aggregate():
    requests = RequestRecords.objects.all().filter(contacted=False)
    work_queue = queue.Queue()
    outputs = []
    for request in requests:
        work_queue.put_nowait(request)

    threads = []
    for i in range(5):
        thread = threading.Thread(
            target=do_work, kwargs={
                'work_queue': work_queue,
            })
        threads.append(thread)

