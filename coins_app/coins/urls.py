"""
Url Patterns for Coins App
"""
from django.urls import path

from .views import CoinsListView

urlpatterns = [
    path('', CoinsListView.as_view(), name='home'),
]
