from django.db import models

# Create your models here.
class RequestRecords(models.Model):
	unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	last_time_checked = models.DateTimeField(help_text='Last time surge pricing was checked')
	phone_number = models.IntegerField(help_text='phone number to contact buyer')
	last_surge_multiplier = models.FloatField(help_text='last surge multiplier recorded')
	surge_threshold = models.FloatField(help_text='surge pricing threshold set by user. Contact if below')
	contacted = models.BooleanField(help_text='have been contacted or not', default=False)

