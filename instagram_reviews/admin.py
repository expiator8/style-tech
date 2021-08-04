from django.contrib import admin
from . import models


@admin.register(models.InstagramReview)
class InstagramReviewAdmin(admin.ModelAdmin):

    """ Instagram Review Admin Definition """

    list_display = (
        "writer",
        "date_created",
        "text",
        "likes",
    )

    list_filter = ("writer",)

    search_fields = ("instagram_products__name",)
