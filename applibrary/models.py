from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import filters

# Create your models here.


class Book(models.Model):
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name=_('Category'),
                                 related_name='FCategory')
    author = models.ForeignKey('Author', verbose_name=_('Author'),  on_delete=models.PROTECT,  related_name='FKAuthor')
    name = models.CharField(max_length=255, verbose_name=_('Book Name'))
    book_published_date = models.IntegerField(verbose_name=_("Book Published Date"))
    stock = models.IntegerField(verbose_name=_('initial stock'), null=True, blank=True,)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="")

    def __str__(self):
        return self.name

    @property
    def total_leased_count_all_time(self):
        result = Lease.objects.filter(book_id=self.id).count()
        return result

    @property
    def current_leased_count(self):
        result = Lease.objects.filter(book_id=self.id).count()-Receive.objects.filter(lease__book_id=self.id).count()
        return result

    @property
    def current_reserved_count(self):
        result = Reserve.objects.filter(book_id=self.id).count()\
                 -CancelReserve.objects.filter(reserve__book_id=self.id).count()
        return result

    @property
    def in_stock(self):
        result = self.stock - self.current_leased_count - self.current_reserved_count
        return result


class Author(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name=_('Author'))

    def __str__(self):
        return self.name

    verbose_name_plural = _('Authors')
    verbose_name = _('Author')


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name=_('Category'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Categoryes')
        verbose_name = _('Category')


class UserIdent(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=50, verbose_name=_('full name'))
    personal_number = models.CharField(max_length=50, verbose_name=_('peronal number'))
    birth_date = models.DateField(verbose_name="birth date")
    is_staff = models.BooleanField()

    def __str__(self):
        return self.user.username


class Lease(models.Model):
    lease_date = models.DateField(verbose_name=_("Lease_date"))
    user = models.ForeignKey(UserIdent, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    must_receive_date = models.DateField(verbose_name=_("must_receive_date"), null=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="")

    def __str__(self):
        return f'user:{self.user.full_name} book:{self.book.name} ' \
               f'leased:{self.lease_date} must_receive_date:{self.must_receive_date}'

    def clean(self):
        if self.book.in_stock < 1:
            raise ValidationError('Not In Stock')


class Receive(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.PROTECT)
    receive_date = models.DateField(verbose_name=_("receive_date"))
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="")

    def __str__(self):
        return f'{self.lease.user.full_name} {self.lease.book.name}'


class Reserve(models.Model):
    reserve_date = models.DateField(verbose_name=_("reserve_date"))
    user = models.ForeignKey(UserIdent, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="")

    def __str__(self):
        return f'book:{self.book.name}  user:{self.user.full_name} '

    def clean(self):
        if self.book.in_stock < 1:
            raise ValidationError('not in stock')


class CancelReserve(models.Model):
    cancel_reserve_date = models.DateField(verbose_name=_("cancel_reserve_date"))
    reserve = models.ForeignKey(Reserve, on_delete=models.PROTECT)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="")

    def __str__(self):
        return f'{self.reserve.book.name} {self.reserve.user.full_name} '

#
# class BookAnalyse(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.PROTECT)
    # @property
    # def book(self):
    #     result = Book.objects.all()
    #     return result

