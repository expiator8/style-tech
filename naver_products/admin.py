from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(
    models.SearchKeyword,
    models.Category,
    models.Seller,
    models.HeelHeight,
    models.MainMaterial,
    models.AddOns,
    models.Feature,
    models.Manufacturer,
    models.Brand,
    models.Gender,
    models.AnkleHeight,
    models.SoleMaterial,
)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.naver_products.count()


class NaverPhotoInline(admin.TabularInline):

    model = models.NaverPhoto


@admin.register(models.NaverProduct)
class NaverProductAdmin(admin.ModelAdmin):

    """ Naver Product Admin Definition """

    inlines = (NaverPhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "search_keywords",
                    "name",
                    "registration",
                    "dibs",
                    "price",
                    "url",
                )
            },
        ),
        (
            "Wide Categories",
            {
                "fields": (
                    "sellers",
                    "categories",
                    "gender",
                    "over_sea_delivery",
                )
            },
        ),
        (
            "Details",
            {
                "classes": ("collapse",),
                "fields": (
                    "manufacturer",
                    "brand",
                    "main_material",
                    "sole_material",
                    "heel_height",
                    "ankle_height",
                    "feature",
                    "add_ons",
                ),
            },
        ),
    )

    list_display = (
        "name",
        "registration",
        "price",
        "dibs",
        "brand",
        "manufacturer",
        "over_sea_delivery",
        "count_search_keywords",
        "count_add_ons",
        "count_feature",
        "count_photos",
        "total_rating",
        "is_newest",
    )

    ordering = (
        "name",
        "registration",
        "price",
        "dibs",
        "brand",
        "manufacturer",
        "gender",
        "over_sea_delivery",
    )

    list_filter = (
        "brand",
        "manufacturer",
        "over_sea_delivery",
        "gender",
        "categories",
        "sellers",
        "heel_height",
        "ankle_height",
        "main_material",
        "sole_material",
    )

    raw_id_fields = ("brand", "manufacturer")

    search_fields = [
        "name",
    ]

    filter_horizontal = (
        "search_keywords",
        "categories",
        "sellers",
        "main_material",
        "sole_material",
        "ankle_height",
        "heel_height",
        "add_ons",
        "feature",
        "gender",
    )

    def count_search_keywords(self, obj):
        return obj.search_keywords.count()

    def count_add_ons(self, obj):
        return obj.add_ons.count()

    count_add_ons.short_description = "Number of Add-Ons"

    def count_feature(self, obj):
        return obj.feature.count()

    count_feature.short_description = "Number of Feature"

    def count_photos(self, obj):
        return obj.naver_photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.NaverPhoto)
class NaverPhotoAdmin(admin.ModelAdmin):

    """ Naver Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
