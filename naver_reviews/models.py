from django.db import models
from core import models as core_models


class NaverReview(core_models.TimeStampedModel):

    """ Naver Review Model Definition """

    naver_review = models.TextField()
    rating = models.IntegerField()
    date_created = models.DateField()
    buy = models.ForeignKey(
        "naver_products.Seller",
        related_name="naver_reviews",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    naver_product = models.ForeignKey(
        "naver_products.NaverProduct",
        related_name="naver_reviews",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.naver_product}"

    class Meta:
        verbose_name_plural = "Naver Reviews"
