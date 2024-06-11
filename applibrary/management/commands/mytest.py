from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from Library.settings import EMAIL_HOST_USER
from applibrary.models import *
from django.db.models import Count


class Command(BaseCommand):
    help = 'send mail wishlist'

    def handle(self, *args, **kwargs):
        # result = Book.objects.annotate(num_leases=Count('lease')).filter(num_leases__gt=0).order_by('-num_leases')
        result = Lease.objects.annotate(num_leases=Count('receive'))
        # result = Book.objects.all()
        for i in result:
            self.stdout.write(i.book.name)

