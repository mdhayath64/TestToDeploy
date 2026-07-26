import uuid
from django.db import models

from core.models import Timestampedmodel
from e_commerce.models import User
from e_commerce.users.models import Subscribers


class Wishlist(Timestampedmodel):
    wishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_wishlist"
    )
    subscriber = models.ForeignKey(
        Subscribers, on_delete=models.CASCADE, related_name="wishlist_subscribers_details"
    )
    item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    item_details = models.JSONField()
    item_added_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.wishlist_id)

