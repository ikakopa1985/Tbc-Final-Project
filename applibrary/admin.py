from django.contrib import admin
from applibrary.models import *
from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import gettext_lazy as _
# Register your models here.


class CategoryFilter(AutocompleteFilter):
    title = 'Category'
    field_name = 'category'


class AuthorFilter(AutocompleteFilter):
    title = 'Author'
    field_name = 'author'


class CurrentLeasedFilter(admin.SimpleListFilter):
    title = _('Current Leased')
    parameter_name = 'current_leased'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(id__in=[book.id for book in queryset if book.current_leased_count > 0])
        if self.value() == 'no':
            return queryset.filter(id__in=[book.id for book in queryset if book.current_leased_count == 0])
        return queryset


class BookFilter(AutocompleteFilter):
    title = 'Book'
    field_name = 'book'


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'book_published_date', 'stock', 'total_leased_count_all_time',
                    'current_leased_count', 'current_reserved_count', 'in_stock')
    list_display_links = ('name',)
    search_fields = ['name', 'author__name', 'category__name']
    list_filter = [CategoryFilter, AuthorFilter, CurrentLeasedFilter]
    autocomplete_fields = ['category', 'author']


class LeaseAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Lease._meta.fields].append('received_date')
    list_display = ('lease_date', 'user', 'book', 'must_receive_date', 'receive_date', 'overdue')
    autocomplete_fields = ['book', 'user']
    list_filter = [BookFilter]
    search_fields = ('user__full_name', 'book__name')


class ReserveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reserve._meta.fields]
    search_fields = ('book__name',)
    autocomplete_fields = ['user', 'book']


class CancelReserveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CancelReserve._meta.fields]
    autocomplete_fields = ['reserve']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = [field.name for field in Category._meta.fields]


class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.fields]
    search_fields = ('name',)


class UserIdentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserIdent._meta.fields]
    search_fields = ('full_name',)
    autocomplete_fields = ['user']


class ReceiveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Receive._meta.fields]
    autocomplete_fields = ['lease']


class WishlistAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wishlist._meta.fields]


admin.site.register(Book, BookAdmin)
admin.site.register(Lease, LeaseAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(CancelReserve, CancelReserveAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(UserIdent, UserIdentAdmin)
admin.site.register(Receive, ReceiveAdmin)
admin.site.register(Wishlist, WishlistAdmin)
