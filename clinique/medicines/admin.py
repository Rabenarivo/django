from django.contrib import admin
from .models import Medicine, StockMovement, Sale, SaleItem , Medicine_stock , Medicine_type


class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = ['created_at']


class MedicineAdmin(admin.ModelAdmin):
    inlines = [StockMovementInline]
    list_display = ['name', 'type', 'stock_min', 'price']

class Medicine_stockAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'quantity_in_stock', 'numero_lot', 'expiration_date']
    readonly_fields = ['created_at']    

class Medicine_typeAdmin(admin.ModelAdmin):
    list_display = ['name']

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
admin.site.register(Medicine_stock)
admin.site.register(Medicine_type)