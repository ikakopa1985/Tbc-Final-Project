from django.core.management.base import BaseCommand
from applibrary.models import *
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'import books from json'

    def handle(self, *args, **kwargs):
        Wishlist.objects.all().delete()
        CancelReserve.objects.all().delete()
        Reserve.objects.all().delete()
        Receive.objects.all().delete()
        Lease.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()

        file_path = str(Path(__file__).resolve().parent) + '\\books_data.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        for book in books_data:
            category, _ = Category.objects.get_or_create(name=book['category'])
            author, _ = Author.objects.get_or_create(name=book['authors'])
            created_book = Book.objects.create(
                name=book['name'],
                author=author,
                category=category,
                book_published_date=int(book['published_date']),
                stock=int(book['stock']),
            )
            self.stdout.write(self.style.SUCCESS(f"Added book : {created_book}"))
