from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(
    models.InstagramHashTag,
    models.SearchedKeyword,
    models.PhotoCaption,
)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.instagram_products.count()


class InstagramPhotoInline(admin.TabularInline):

    model = models.InstagramPhoto


@admin.register(models.InstagramProduct)
class InstagramProductAdmin(admin.ModelAdmin):

    """ Instagram ProductAdmin Admin Definition """

    inlines = (InstagramPhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "writer",
                    "date_created",
                    "likes",
                    "visits",
                    "searched_keywords",
                    "url",
                )
            },
        ),
        (
            "Detail Info",
            {
                "fields": (
                    "text",
                    "is_ad",
                    "instagram_hash_tags",
                )
            },
        ),
    )

    list_display = (
        "writer",
        "date_created",
        "likes",
        "count_hash_tags",
        "count_photos",
        "is_ad",
        "is_newest",
    )

    ordering = (
        "writer",
        "date_created",
        "likes",
        "is_ad",
    )

    list_filter = ("is_ad",)

    search_fields = [
        "instagram_hash_tags__name",
    ]

    filter_horizontal = ("instagram_hash_tags", "searched_keywords")

    def count_hash_tags(self, obj):
        return obj.instagram_hash_tags.count()

    count_hash_tags.short_description = "Hash Tag Count"

    def count_photos(self, obj):
        return obj.instagram_photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.InstagramPhoto)
class InstagramPhotoAdmin(admin.ModelAdmin):

    """ Instagram Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")
    filter_horizontal = ("caption",)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
