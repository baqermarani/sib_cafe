from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail
from django.core.exceptions import ValidationError

# Create your models here.


class Food(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100, unique=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    food_image = ImageField(upload_to='food/%Y/%m/', null=True, blank=True)
    date_added = models.DateTimeField(verbose_name=_("date added"), auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name=_("date modified"), auto_now=True)

    class Meta:
        db_table = 'food'
        verbose_name = _('food')
        verbose_name_plural = _('food')

    def save(self, *args, **kwargs):
        if self.food_image:
            self.image = get_thumbnail(self.food_image, '500x600', quality=99, format='JPEG')
        super(Food, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class FoodItem(models.Model):
    class Day(models.TextChoices):
        EVERYDAY = 0, _("everyday")
        SATURDAY = 1, _("saturday")
        SUNDAY = 2, _("sunday")
        MONDAY = 3, _("monday")
        TUESDAY = 4, _("tuesday")
        WEDNESDAY = 5, _("wednesday")

    class FoodType(models.TextChoices):
        SUBSIDY = 1, _("subsidy")
        NOTSUBSIDY = 2, _("non-subsidy")

    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food_items')
    amount_of_store = models.PositiveSmallIntegerField(verbose_name=_('storage'), default=10, )
    day = models.CharField(verbose_name=_('day'), choices=Day.choices, max_length=1)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    date_modified = models.DateTimeField(_("date modified"), auto_now=True)
    price = models.PositiveIntegerField(_('price'), default=1000)
    food_type = models.CharField(max_length=10, choices=FoodType.choices, default=1)

    class Meta:
        db_table = 'food_item'
        verbose_name = _('food item')
        verbose_name_plural = _('food items')
        unique_together = ('food', 'day')

    def __str__(self):
        return f'{self.food}'

    def clean(self):
        if FoodItem.objects.filter(food=self.food, day=self.Day.EVERYDAY).exists():
            raise ValidationError('Food Already Exists')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(FoodItem, self).save(*args, **kwargs)
