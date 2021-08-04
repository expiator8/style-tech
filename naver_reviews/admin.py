from django.contrib import admin
from . import models


@admin.register(models.NaverReview)
class NaverReviewAdmin(admin.ModelAdmin):

    """ Naver Review Admin Definition """

    list_display = (
        "date_created",
        "rating",
        "naver_review",
        "buy",
    )

    list_filter = ("rating",)

    search_fields = ("naver_product__name",)
