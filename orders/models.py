from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from core.models import FoodItem
from accounts.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Order(models.Model):
    class OrderState(models.TextChoices):
        PENDING = 0, _('order pending')
        SUBMITTED = 1, _("order submitted")
        SERVERD = 2, _("order served")
        PAYED = 3, _("order payed")
        CANCELED = -1, _("order cancelled")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(_("state"), max_length=2, choices=OrderState.choices, default=OrderState.SUBMITTED)

    class Meta:
        ordering = ('paid', '-updated')
        db_table = 'order'

    def __str__(self):
        return f'{self.user.full_name} - {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'Order-item'

    @property
    def price(self):
        return self.item.price

    @property
    def get_cost(self):
        return self.item.price * self.quantity

    def validate_item_number(self):
        if self.item.food_type == '1' and self.quantity > 1:
            raise ValidationError(_("you can not Order more than 1 !"))

    def clean(self):
        self.validate_item_number()
        super(OrderItem, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(OrderItem, self).save(*args, **kwargs)
