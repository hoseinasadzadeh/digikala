from django.contrib import admin
from . import models


admin.site.register(models.ShippingAddress)
admin.site.register(models.OrderItem)


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['date_ordered', 'last_update']
    inlines = [OrderItemInline]
