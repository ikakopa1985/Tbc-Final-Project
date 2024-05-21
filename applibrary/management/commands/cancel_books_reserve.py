from django.core.management.base import BaseCommand
from applibrary.models import *
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'cancel book reservations'

    def handle(self, *args, **kwargs):
        for item in Reserve.objects.all():
            if ((date.today() - item.reserve_date) > timedelta(days=1)) and (
                    item not in [x.reserve for x in CancelReserve.objects.all()]):
                cancel_reserve_item = CancelReserve.objects.create(
                    cancel_reserve_date=date.today(),
                    reserve=item,
                )
                self.stdout.write(self.style.SUCCESS(f"canceled Reserved book : {item}"))
