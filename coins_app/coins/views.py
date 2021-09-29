"""
Views for Coins App
"""
from django.db.models import F, Sum
from django.views.generic import ListView

from .models import Coin


class CoinsListView(ListView):
    """
    View Books
    """
    model = Coin
    context_object_name = "coins"
    template_name = "index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(year=F("release_date__year"))

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['coins_count'] = context["coins"].count()
        context['coins_sum'] = context["coins"].aggregate(Sum("price"))["price__sum"]
        return context
