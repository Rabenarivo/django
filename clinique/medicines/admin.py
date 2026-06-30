from django.contrib import admin
from .models import Medicine, StockMovement, Sale, SaleItem


class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = ['created_at']


class MedicineAdmin(admin.ModelAdmin):
    inlines = [StockMovementInline]
    list_display = ['name', 'quantity_in_stock', 'price', 'expiration_date']


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ['id', 'patient', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        sale = form.instance
        sale.calculate_total()


admin.site.register(Medicine, MedicineAdmin)
admin.site.register(StockMovement)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)
