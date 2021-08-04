from django.db import models
from core import models as core_models


class InstagramReview(core_models.TimeStampedModel):

    """ Instagram Review Model Definition """

    text = models.TextField()
    date_created = models.DateField()
    likes = models.IntegerField(default=0)
    instagram_product = models.ForeignKey(
        "instagram_products.InstagramProduct",
        related_name="instagram_reviews",
        on_delete=models.CASCADE,
    )
    writer = models.ForeignKey(
        "instagram_users.InstagramUser",
        related_name="instagram_reviews",
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.instagram_product}"

    class Meta:
        verbose_name = "Instagram Review"
