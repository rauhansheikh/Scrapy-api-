from django.urls import path
from .views import search_page, SearchAPIView
from . import views

urlpatterns = [
    path('', search_page, name='search-page'),
    path('api/search/', SearchAPIView.as_view(), name='search-api'),
    path("rescrape/<int:result_id>/", views.rescrape_link, name="rescrape_link"),
]
