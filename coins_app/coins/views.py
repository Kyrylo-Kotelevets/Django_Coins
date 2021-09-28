"""
Views for Coins App
"""
from django.views.generic import ListView

from .models import Coin


class CoinsListView(ListView):
    """
    View Books
    """
    model = Coin
    context_object_name = "coins"
    template_name = "index.html"
