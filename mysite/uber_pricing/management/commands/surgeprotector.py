from django.core.management import BaseCommand

from uber_pricing import crawler


class Command(BaseCommand):
    help = "Run the sensor21 aggregator once."

    def handle(self, *args, **options):
        crawler.aggregate()