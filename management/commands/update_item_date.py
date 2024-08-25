# BE-vehicle/management/commands/update_item_dates.py

from django.core.management.base import BaseCommand
from item.models import Item
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Update all item dates from UTC to CST'

    def handle(self, *args, **kwargs):
        # Fetch all items
        items = Item.objects.all()

        for item in items:
            # Parse existing date
            utc_date = datetime.strptime(item.date, "%Y-%m-%dT%H:%M:%S.%fZ")
            # Convert to China Standard Time (CST)
            cst_date = utc_date + timedelta(hours=8)
            # Format it back to string
            item.date = cst_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            item.save()
        
        self.stdout.write(self.style.SUCCESS("Successfully updated all item dates to CST"))
