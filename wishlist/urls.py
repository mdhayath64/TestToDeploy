from django.urls import path
from wishlist.views.wishlist import WishlistView

urlpatterns = [
    path('', WishlistView.as_view()),
]

