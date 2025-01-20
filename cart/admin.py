# Register your models here.
from django.contrib import admin
from .models import Vegetable, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'total_amount', 'complete')
    list_filter = ('complete', 'date_ordered')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)

admin.site.register(Vegetable, VegetableAdmin)
admin.site.register(Order, OrderAdmin)
