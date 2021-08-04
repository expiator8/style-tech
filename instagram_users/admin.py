from django.contrib import admin
from . import models


@admin.register(models.InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):

    """ Instagram User Admin Definition """

    list_display = (
        "insta_id",
        "is_influencer",
        "followers",
        "followings",
    )

    list_filter = ("is_influencer",)

    search_fields = ("insta_id",)
