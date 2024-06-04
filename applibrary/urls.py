"""
URL configuration for Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applibrary.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'books', BookViewSet,  basename='BookViewSet'),
router.register(r'users', UserIdentViewSet, basename='UserIdentViewSet'),
router.register(r'reserves', ReserveViewSet, basename='ReserveViewSet'),
router.register(r'wishlist', WishlistViewSet, basename='WishlistViewSet'),


urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("index/", index, name='index'),
    path("get10PopularBooks/", Get10PopularBooksView.as_view(), name='Get10PopularBooks'),
    path("getAllBookLease1Year/", GetAllBookLease1Year.as_view(), name='GetAllBookLease1Year'),
    path("get100BookMostOverdue/", Get100BookMostOverdue.as_view(), name='get100BookMostOverdue'),
    path("get100UserMostOverdue/", Get100UserMostOverdue.as_view(), name='Get100UserMostOverdue'),
    path("getSortedBooks/", GetSortedBooks.as_view(), name='GetSortedBooks'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-profile/', UserProfileView.as_view(), name='user_profile'),
]
