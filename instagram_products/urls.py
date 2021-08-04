from django.urls import path
from . import views


app_name = "instagram_products"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    path("scrape", views.ScrapeView.as_view(), name="scrape"),
    path("detail/<int:pk>", views.InstagramProductDetail.as_view(), name="detail"),
]
