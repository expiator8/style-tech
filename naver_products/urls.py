from django.urls import path
from . import views


app_name = "naver_products"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    path("api/chart/data", views.ChartView.as_view(), name="chart-data"),
    path("scrape", views.ScrapeView.as_view(), name="scrape"),
    path("detail/<int:pk>", views.NaverProductDetail.as_view(), name="detail"),
]
