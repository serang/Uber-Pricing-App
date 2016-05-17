
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def job():
    subprocess.Popen(["python3", "manage.py", "surgeprotector"])


class Command(BaseCommand):
    help = "Start the SurgeProtector checking process"

    def handle(self, *args, **options):
        sched.start()