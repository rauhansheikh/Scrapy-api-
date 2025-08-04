from django.urls import path
from .views import search_page, SearchAPIView

urlpatterns = [
    path('', search_page, name='search-page'),
    path('api/search/', SearchAPIView.as_view(), name='search-api'),
]
