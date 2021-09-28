"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Coin
from django.utils.html import format_html


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    """
    Admin Model Settings
    """

    def obverse_img(self, obj):
        return format_html(f"<img width=\"80px\" height=\"80px\" src={obj.obverse.url} />")

    obverse_img.short_description = "obverse"

    def reverse_img(self, obj):
        return format_html(f"<img width=\"80px\" height=\"80px\" src={obj.reverse.url} />")

    reverse_img.short_description = "reverse"

    def formatted_date(self, obj):
        return obj.release_date.strftime("%Y-%m-%d")

    formatted_date.short_description = "release date"

    def formatted_price(self, obj):
        return format_html(f"<b style=\"font-size: 15px\">{obj.price}</b>")

    formatted_price.short_description = "Price"

    list_filter = ("series", "circulation", "metal")
    search_fields = ("title",)
    list_display = ("formatted_date", "title", "circulation", "formatted_price",
                    "obverse_img", "reverse_img")
    readonly_fields = ("obverse_img", "reverse_img")
