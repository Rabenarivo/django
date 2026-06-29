from django.contrib import admin
from .models import Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


class PrescriptionAdmin(admin.ModelAdmin):
    inlines = [PrescriptionItemInline]


admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionItem)