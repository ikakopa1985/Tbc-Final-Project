from django.contrib import admin
from applibrary.models import *
from admin_auto_filters.filters import AutocompleteFilter
# Register your models here.


class CategoryFilter(AutocompleteFilter):
    title = 'Category'
    field_name = 'category'


class AuthorFilter(AutocompleteFilter):
    title = 'Author'
    field_name = 'author'


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'book_published_date', 'stock', 'total_leased_count_all_time',
                    'current_leased_count', 'current_reserved_count', 'in_stock')
    list_display_links = ('name',)
    search_fields = ['name', 'author__name', 'category__name']
    list_filter = [CategoryFilter, AuthorFilter]
    autocomplete_fields = ['category', 'author']


class LeaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lease._meta.fields]
    autocomplete_fields = ['book', 'user']
    list_filter = ('book',)
    search_fields = ('user', 'book')


class ReserveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reserve._meta.fields]
    search_fields = ('book',)
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
    search_fields = ('user',)
    autocomplete_fields = ['user']


# class BookAnalyseAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Book._meta.fields]
#     list_display = ('book',)
#     autocomplete_fields = ['author', 'category']
#     # search_fields = ('user',)
#     # autocomplete_fields = ['user']


class ReceiveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Receive._meta.fields]
    # autocomplete_fields = ['author', 'category']
    # search_fields = ('user',)
    autocomplete_fields = ['lease']



admin.site.register(Book, BookAdmin)
admin.site.register(Lease, LeaseAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(CancelReserve, CancelReserveAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(UserIdent, UserIdentAdmin)
admin.site.register(Receive, ReceiveAdmin)
# admin.site.register(BookAnalyse, BookAnalyseAdmin)
