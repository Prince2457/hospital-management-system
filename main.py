from utils.billing import create_bill, get_all_billing
from utils.inventory import create_inventory, get_all_inventory
from utils.medical_records import create_record, get_all_medical_records

# Test billing
create_bill(2, 1, 'Consultation', 150.00, 'pending', None)

# Test inventory
create_inventory('Paracetamol', 'medicine', 100, 20, 2.50)

# Test medical records
create_record(2, 1, 1, 'Hypertension', 'Rest and medication', 'Blood pressure test', 'Monitor weekly')

# View all
bills = get_all_billing()
print(f"Bills: {len(bills)} found")

items = get_all_inventory()
print(f"Inventory: {len(items)} found")

records = get_all_medical_records()
print(f"Medical records: {len(records)} found")

