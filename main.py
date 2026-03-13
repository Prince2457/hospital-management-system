from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Billing
from models.inentory import Inventory
from models.medical_records import MedicalRecords

# create a patient object
p1 = Patient(
    patient_id=1,
    full_name="John Mensah",
    ghana_card_number="GHA-123456789",
    date_of_birth="1990-05-15",
    gender="male",
    phone="0244123456"
)

# create a doctor object
d1 = Doctor(
    doctor_id=1,
    full_name="Kwame Asante",
    license_number="LIC-001",
    specialization="Cardiology",
    consultation_fee=150.00
)

a1 = Appointment(
    appointment_id=1,
    patient_id=1,
    doctor_id=1,
    appointment_date="2026-03-13",
    appointment_time="9:00:00"
)

b1 = Billing(
    bill_id=1,
    patient_id=1,
    appointment_id=1,
    bill_item="Medical bill",
    amount=5.00
)

i1 = Inventory(
    item_id=1,
    item_name="Surgical gloves",
    item_category="Supplies",
    quantity=60,
    reorder_level=20, 
    item_cost=5.00
)

m1 = MedicalRecords(
    record_id=1,
    patient_id=1,
    doctor_id=1,
    appointment_id=1,
    diagnosis="Hypertension",
    treatment="Rest and medication",
    lab_test="Blood pressure test",
    notes="monitor weekly",
)
# print both
print(p1)
print(d1)
print(a1)
print(b1)
print(i1)
print(m1)