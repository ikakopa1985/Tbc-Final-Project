from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from Library.settings import EMAIL_HOST_USER
from applibrary.models import *


class Command(BaseCommand):
    help = 'send mail wishlist'

    def handle(self, *args, **kwargs):
        for item in Wishlist.objects.all():
            if item.book.in_stock > 0:
                subject = f'Dear {item.user.full_name}'
                body = f' <h3> library has received the book You Wished "{item.book.name}"  ' \
                       f'And there are currently {item.book.in_stock} copies of it in stock </h3>'

                email_from = EMAIL_HOST_USER
                recipient_list = [item.user.user.email]
                email = EmailMessage(subject, body, email_from, recipient_list)
                email.content_subtype = "html"
                email.send()
                self.stdout.write(self.style.SUCCESS(f'{item.user.user.email} sent'))

