from django.core.management.base import BaseCommand
from medicines.models import Medicine_type, Medicine, Medicine_stock
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with initial Medicine types, Medicines, and Stock.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding medicine types...")
        
        # 1. Create Types
        types_data = ['Antibiotique', 'Antalgique', 'Anti-inflammatoire', 'Vitamine', 'Antiseptique', 'Sirop']
        created_types = {}
        for t in types_data:
            type_obj, created = Medicine_type.objects.get_or_create(name=t)
            created_types[t] = type_obj
            
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(types_data)} medicine types."))

        # 2. Create Medicines
        self.stdout.write("Seeding medicines...")
        medicines_data = [
            {'name': 'Paracétamol 500mg', 'type': created_types['Antalgique'], 'stock_min': 50, 'price': 5000, 'description': 'Soulage la douleur et la fièvre'},
            {'name': 'Amoxicilline 1g', 'type': created_types['Antibiotique'], 'stock_min': 20, 'price': 15000, 'description': 'Antibiotique à large spectre'},
            {'name': 'Ibuprofène 400mg', 'type': created_types['Anti-inflammatoire'], 'stock_min': 30, 'price': 8000, 'description': 'Anti-inflammatoire non stéroïdien'},
            {'name': 'Vitamine C 1000mg', 'type': created_types['Vitamine'], 'stock_min': 10, 'price': 4500, 'description': 'Complément de vitamine C'},
            {'name': 'Bétadine 10%', 'type': created_types['Antiseptique'], 'stock_min': 15, 'price': 6000, 'description': 'Solution antiseptique pour plaies'},
            {'name': 'Sirop Contre la Toux', 'type': created_types['Sirop'], 'stock_min': 25, 'price': 7500, 'description': 'Sirop expectorant'},
        ]
        
        created_medicines = {}
        for m in medicines_data:
            med_obj, created = Medicine.objects.get_or_create(
                name=m['name'],
                defaults={
                    'type': m['type'],
                    'stock_min': m['stock_min'],
                    'price': m['price'],
                    'description': m['description']
                }
            )
            created_medicines[m['name']] = med_obj

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(medicines_data)} medicines."))

        # 3. Create Stocks (Arrivages)
        self.stdout.write("Seeding medicine stocks (batches)...")
        
        today = timezone.now().date()
        
        stocks_data = [
            # Paracetamol: One good lot, one expiring soon
            {'medicine': created_medicines['Paracétamol 500mg'], 'qty': 100, 'lot': 'LOT-PARA-001', 'exp': today + timedelta(days=730)},
            {'medicine': created_medicines['Paracétamol 500mg'], 'qty': 20, 'lot': 'LOT-PARA-002', 'exp': today + timedelta(days=15)}, # Expire très bientôt
            
            # Amoxicilline: Normal stock
            {'medicine': created_medicines['Amoxicilline 1g'], 'qty': 40, 'lot': 'LOT-AMOX-001', 'exp': today + timedelta(days=365)},
            
            # Ibuprofène: Low stock (below min_stock of 30)
            {'medicine': created_medicines['Ibuprofène 400mg'], 'qty': 10, 'lot': 'LOT-IBUP-001', 'exp': today + timedelta(days=500)}, # Stock faible
            
            # Vitamine C: Already expired
            {'medicine': created_medicines['Vitamine C 1000mg'], 'qty': 50, 'lot': 'LOT-VITC-001', 'exp': today - timedelta(days=10)}, # Déjà périmé
            
            # Bétadine
            {'medicine': created_medicines['Bétadine 10%'], 'qty': 30, 'lot': 'LOT-BETA-001', 'exp': today + timedelta(days=800)},
        ]

        count_stock = 0
        for s in stocks_data:
            # check if stock lot exists so we don't duplicate on multiple runs
            stock_obj, created = Medicine_stock.objects.get_or_create(
                numero_lot=s['lot'],
                defaults={
                    'medicine': s['medicine'],
                    'quantity_in_stock': s['qty'],
                    'expiration_date': s['exp']
                }
            )
            if created:
                count_stock += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count_stock} new stock batches."))
        self.stdout.write(self.style.SUCCESS("Done! Your pharmacy is now populated with test data."))
