from datetime import datetime
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from applibrary.models import *
from applibrary.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'author__name']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'author__name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class UserIdentViewSet(viewsets.ModelViewSet):
    queryset = UserIdent.objects.all()
    serializer_class = UserIdentSerializer


class ReserveViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

    def perform_create(self, serializer):
        user_recognized = UserIdent.objects.get(user=self.request.user)
        serializer.save(user=user_recognized)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def perform_create(self, serializer):
        user_recognized = UserIdent.objects.get(user=self.request.user)
        serializer.save(user=user_recognized)


def index(request):
    return render(request, template_name='applibrary/index.html')


class Get10PopularBooksView(ListCreateAPIView):
    serializer_class = Get10PopularBookSerializer

    def get_queryset(self):
        queryset = (
            Book.objects.annotate(lease_count=Count('lease'))
            .order_by('-lease_count')[:10]
        )
        return queryset


class GetAllBookLease1Year(ListCreateAPIView):
    serializer_class = GetAllBookLease1YearSerializer

    def get_queryset(self):
        current_year = datetime.now().year
        queryset = (
            Book.objects.annotate(
                lease_count=Count('lease', filter=ExtractYear('lease__lease_date') == current_year)
            ).order_by('-lease_count')
        )
        return queryset


class Get100BookMostOverdue(ListCreateAPIView):
    serializer_class = Get100BookMostOverdueSerializer

    def get_queryset(self):
        queryset = Book.objects.raw('''
        select *,  Cast ((
            JulianDay(applibrary_receive.receive_date) - JulianDay(al.must_receive_date)
        ) As Integer) as overdueDay
        from applibrary_receive
        join applibrary_lease al on applibrary_receive.lease_id = al.id
        join applibrary_book ab on ab.id = al.book_id
        where Cast ((
            JulianDay(applibrary_receive.receive_date) - JulianDay(al.must_receive_date)
        ) As Integer) > 1
        order by Cast ((
            JulianDay(applibrary_receive.receive_date) - JulianDay(al.must_receive_date)
        ) As Integer) 
        LIMIT 100
        ''')
        return queryset


class Get100UserMostOverdue(ListCreateAPIView):
    serializer_class = Get100UserMostOverdueSerializer

    def get_queryset(self):
        queryset = Book.objects.raw('''
            select *,  Cast ((
                JulianDay(applibrary_receive.receive_date) - JulianDay(al.must_receive_date)
            ) As Integer) as overdueDay, au.full_name
             as full_name, a.username as username,  count(a.username) as user_overdue_count
            from applibrary_receive
            join applibrary_lease al on applibrary_receive.lease_id = al.id
            join applibrary_book ab on ab.id = al.book_id
            join applibrary_userident au on al.user_id = au.id
            join auth_user a on au.user_id = a.id
            where Cast ((
                JulianDay(applibrary_receive.receive_date) - JulianDay(al.must_receive_date)
            ) As Integer) > 1
            GROUP BY a.username
            ORDER BY -user_overdue_count
            LIMIT 100
        ''')
        return queryset


class GetSortedBooks(ListCreateAPIView):
    serializer_class = GetSortedBooksSerializer

    def get_queryset(self):
        most_leased_books = Book.objects.annotate(num_leases=Count('lease'))\
            .filter(num_leases__gt=0).order_by('-num_leases')
        return most_leased_books

