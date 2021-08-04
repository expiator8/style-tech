from django.db import models
from django.urls import reverse
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SearchKeyword(AbstractItem):

    """ Naver Search Keyword Model Definition """

    class Meta:
        verbose_name_plural = "Search Keywords"
        ordering = ["name"]


class Category(AbstractItem):

    """ Category Model Definition """

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Seller(AbstractItem):

    """ Seller Model Definiton """

    pass


class HeelHeight(AbstractItem):

    """ Heel Height Model Definiton """

    class Meta:
        verbose_name_plural = "Heel Height"


class MainMaterial(AbstractItem):

    """ Main Material Model Definiton """

    class Meta:
        verbose_name_plural = "Main Material"


class AddOns(AbstractItem):

    """ Add-Ons Model Definiton """

    class Meta:
        verbose_name_plural = "Add-Ons"


class Feature(AbstractItem):

    """ Feature Model Definiton """

    class Meta:
        verbose_name_plural = "Feature"


class Manufacturer(AbstractItem):

    """ Manufacturer Model Definition """

    pass


class Brand(AbstractItem):

    """ Brand Model Definition """

    pass


class Gender(AbstractItem):

    """ Gender Model Definition """

    class Meta:
        verbose_name_plural = "Gender"


class AnkleHeight(AbstractItem):

    """ AnkleHeight Model Definition """

    class Meta:
        verbose_name_plural = "Ankle Height"


class SoleMaterial(AbstractItem):

    """ Sole Material Model Definition """

    class Meta:
        verbose_name_plural = "Sole Material"


class NaverPhoto(core_models.TimeStampedModel):

    """ Naver Photo Model Definition """

    file = models.ImageField(upload_to="naver_photos")
    naver_product = models.ForeignKey(
        "NaverProduct", related_name="naver_photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.naver_product}"

    class Meta:
        verbose_name_plural = "Naver Photos"


class NaverProduct(core_models.TimeStampedModel):

    """ Naver Product Model Definition """

    name = models.CharField(max_length=100)
    registration = models.DateField(blank=True, default="", null=True)
    dibs = models.IntegerField()
    url = models.CharField(max_length=1500)
    price = models.IntegerField()
    over_sea_delivery = models.BooleanField(default=False)

    search_keywords = models.ManyToManyField(
        "SearchKeyword", related_name="naver_products", blank=True
    )
    categories = models.ManyToManyField(
        "Category", related_name="naver_products", blank=True
    )
    sellers = models.ManyToManyField(
        "Seller", related_name="naver_products", blank=True
    )
    heel_height = models.ManyToManyField(
        "HeelHeight", related_name="naver_products", blank=True
    )
    ankle_height = models.ManyToManyField(
        "AnkleHeight", related_name="naver_products", blank=True
    )
    main_material = models.ManyToManyField(
        "MainMaterial", related_name="naver_products", blank=True
    )
    sole_material = models.ManyToManyField(
        "SoleMaterial", related_name="naver_products", blank=True
    )
    gender = models.ManyToManyField("Gender", related_name="naver_products", blank=True)
    add_ons = models.ManyToManyField(
        "AddOns", related_name="naver_products", blank=True
    )
    feature = models.ManyToManyField(
        "Feature", related_name="naver_products", blank=True
    )
    manufacturer = models.ForeignKey(
        "Manufacturer",
        related_name="naver_products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        "Brand",
        related_name="naver_products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Naver Products"

    def get_absolute_url(self):
        return reverse("naver_products:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.naver_reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        (photo,) = self.naver_photos.all()[:1]
        return photo.file.url

    def is_newest(self):
        return self.created == self.updated

    is_newest.boolean = True
