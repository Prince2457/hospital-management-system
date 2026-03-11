from utils.doctors import get_all_doctors, create_doctor

create_doctor(1, 'Cardiology', 'MBChB', 'LIC-001', 'Heart Center', 'Monday,Wednesday,Friday', 150.00)

doctors = get_all_doctors()
print(f"\nAll doctors ({len(doctors)} found):")
for doctor in doctors:
    print(f"{doctor['doctor_id']} - {doctor['specialization']} - {doctor['department']}")