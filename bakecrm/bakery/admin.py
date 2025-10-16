from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'created_at']
	readonly_fields = ['image_preview']
	search_fields = ['name']

	def image_preview(self, obj):
		if obj.image:
			return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;">')
		return "Нет изображения"
	image_preview.short_description = 'Превью'

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ['price_at_time']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'status', 'total_amount', 'created_by', 'created_at']
	list_filter = ['status', 'created_at', 'created_by']
	inlines = [OrderItemInline]
	readonly_fields = ['created_at', 'updated_at', 'created_by']

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		super().save_model(request, obj, form, change)