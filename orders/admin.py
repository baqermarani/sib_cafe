from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	fieldsets = [
		('item', {'fields': ['item'], }),
		('Quantity', {'fields': ['quantity'], }),
		('Price', {'fields': ['price'], }),
		('total', {'fields': ['get_cost'], }),
	]
	raw_id_fields = ['item']
	readonly_fields = ['price', 'get_cost']
	can_delete = True
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'created', 'state']
	list_display_links = ('id', 'user')
	list_filter = ['created', 'state', 'paid', ]
	search_fields = ['paid', 'user', ]
	fieldsets = [
		('Order Information', {'fields': ['user', 'created', 'state'], }),
	]
	readonly_fields = ['created']

	inlines = [
		OrderItemAdmin,
	]
