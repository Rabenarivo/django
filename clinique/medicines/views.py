from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, StockMovement, Sale
from .forms import MedicineForm, SaleStatusForm
from django.contrib.auth.decorators import login_required


@login_required
def chabge_statut_sale(request, sale_id):
    print(f"[DEBUG] change_statut_sale called for sale {sale_id}")  # Debug
    sale = get_object_or_404(Sale, id=sale_id)
    
    if request.method == "POST":
        print(f"[DEBUG] POST request received with data: {request.POST}")  # Debug
        form = SaleStatusForm(request.POST, instance=sale)
        print(f"[DEBUG] Form valid: {form.is_valid()}")  # Debug
        if not form.is_valid():
            print(f"[DEBUG] Form errors: {form.errors}")  # Debug
        
        if form.is_valid():
            updated_sale = form.save()
            print(f"[DEBUG] Saved sale, new status: {updated_sale.status}")  # Debug
            
            # If status changed to COMPLETED, create StockMovements if not already created
            if updated_sale.status == "COMPLETED":
                for sale_item in updated_sale.items.all():
                    if not StockMovement.objects.filter(
                        medicine=sale_item.medicine,
                        movement_type="OUT",
                        reference=f"Sale {updated_sale.id}",
                    ).exists():
                        StockMovement.objects.create(
                            medicine=sale_item.medicine,
                            movement_type="OUT",
                            quantity=sale_item.quantity,
                            reference=f"Sale {updated_sale.id}",
                        )
                        print(f"[DEBUG] Created StockMovement for item {sale_item.id}")
            return redirect("list_sales")
    else:
        print(f"[DEBUG] GET request, initial status: {sale.status}")
        form = SaleStatusForm(instance=sale)
    
    return render(
        request,
        "medicines/change_statut_sale.html",
        {"sale": sale, "form": form},
    )


@login_required
def list_sales(request):
    sales = Sale.objects.filter(status="PENDING")
    return render(request, "medicines/list_sales.html", {"sales": sales})