from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, StockMovement, Sale
from .forms import MedicineForm, SaleStatusForm, Medicine_stockForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_pharmacist(user):
    return hasattr(user, 'profile') and user.profile.role == 'PHARMARMACIST'



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

@login_required
@user_passes_test(is_pharmacist)
def create_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            return redirect("create_medicine_stock_1", medicine_id=medicine.id)
    else:
        form = MedicineForm()
    return render(request, "medicines/create_medicine.html", {"form": form})

@login_required
@user_passes_test(is_pharmacist)
def create_medicine_stock(request, medicine_id=None):
    initial_data = {}
    if medicine_id:
        initial_data['medicine'] = get_object_or_404(Medicine, id=medicine_id)
        
    if request.method == "POST":
        form = Medicine_stockForm(request.POST)
        if form.is_valid():
            medicine_stock = form.save()
            StockMovement.objects.create(
                medicine=medicine_stock.medicine,
                movement_type="IN",
                quantity=medicine_stock.quantity_in_stock,
                reference=f"Stock {medicine_stock.id}",
            )
            return redirect("create_medicine") # Redirection temporaire
    else:
        form = Medicine_stockForm(initial=initial_data)
    return render(request, "medicines/create_medicine_stock.html", {"form": form})
