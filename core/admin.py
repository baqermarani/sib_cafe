from django.contrib import admin

# Register your models here.
from core.models import FoodItem, Food


class FoodItemInline(admin.StackedInline):
    model = FoodItem
    extra = 0


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'food_image', ]
    list_filter = ['title', ]
    sortable_by = ['title', ]
    inlines = [FoodItemInline,]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'food', 'day', ]
    list_display_links = ['food']
    list_filter = ['day', ]
    search_fields = ['day',]
