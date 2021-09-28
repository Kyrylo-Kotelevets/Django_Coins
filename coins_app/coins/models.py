"""
The module is used to describe database Coin model
"""
from datetime import date

from typing import Optional
from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)


class Coin(models.Model):
    """
    Entity Model Coin
    """
    NOMINALS = (
        (2, 2),
        (5, 5),
        (10, 10),
        (200000, 200000)
    )
    title = models.CharField(max_length=256, null=False, blank=False)
    release_date = models.DateField(auto_now=False, auto_now_add=False)

    short_title = models.CharField(max_length=256, null=False, blank=False)
    nominal = models.IntegerField(choices=NOMINALS, null=False, blank=False)
    series = models.CharField(max_length=256, null=False, blank=False)
    circulation = models.IntegerField(null=False, blank=False)
    metal = models.CharField(max_length=64, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    diameter = models.FloatField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    existence = models.BooleanField(default=False, null=False, blank=False)

    obverse = models.ImageField(upload_to="coins_obverse")
    reverse = models.ImageField(upload_to="coins_reverse")

    def __str__(self) -> str:
        """
        Function for line display of the model
        """
        return f"{self.release_date} «{self.title}»"

    def save(self, *args, **kwargs) -> None:
        """
        Overridden save method for setting up the short title
        """
        if not self.short_title:
            self.short_title = self.title
        super().save(*args, **kwargs)

    @classmethod
    def get(cls, title: str, year: int) -> Optional["Coin"]:
        """
        Function for retrieving coin by title and release year.

        Parameters
        ----------
        title : str
            Coin title
        year : int
            Coin release date year

        Returns
        -------
        Optional["Coin"]
            Coin with matching title and year if such exists
        """
        return cls.objects.filter(title=title, release_date__year=year).first()

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Coin"
        ordering = ("-release_date", "title")
        constraints = [
            models.UniqueConstraint(
                name="%(class)s_unique",
                fields=["release_date", "title"],
            ),
            models.CheckConstraint(
                name="%(class)s_title_too_short",
                check=models.Q(title__length__gt=1)
            ),
            models.CheckConstraint(
                name="%(class)s_release_date_too_old",
                check=models.Q(release_date__gt=date(1995, 1, 1))
            ),
        ]
