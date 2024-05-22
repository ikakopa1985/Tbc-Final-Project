from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from applibrary.models import *
from Library.settings import EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'send mail'

    def handle(self, *args, **kwargs):
        queryset = Book.objects.raw('''
        select applibrary_lease.id as id,  au.full_name, a.email, ab.name, Cast ((
            JulianDay(date('now')) - JulianDay(applibrary_lease.must_receive_date)
        ) As Integer) as overdueDay
        from applibrary_lease
        left outer join applibrary_receive ar on applibrary_lease.id = ar.lease_id
        join applibrary_book ab on applibrary_lease.book_id = ab.id
        join applibrary_userident au on applibrary_lease.user_id = au.id
        join auth_user a on au.user_id = a.id
        where (ar.id is null)
          and Cast ((
                    JulianDay(JulianDay(applibrary_lease.must_receive_date) - date('now'))
                ) As Integer) > 1
                ''')

        for item in queryset:
            subject = f'Dear {item.full_name}'
            body = f'<p> <h1>Please Return book </h1> <br><h3>{item.name} </h1> <br> overdue day is {item.overdueDay}' \
                   f' day, <br>  <br></p>'
            email_from = EMAIL_HOST_USER
            recipient_list = [item.email]

            email = EmailMessage(subject, body, email_from, recipient_list)
            email.content_subtype = "html"
            email.send()
            self.stdout.write(self.style.SUCCESS(f'{item.email} sent'))

