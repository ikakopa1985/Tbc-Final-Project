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


class UserIdentViewSet(viewsets.ModelViewSet):
    queryset = UserIdent.objects.all()
    serializer_class = UserIdentSerializer


class ReserveViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

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

