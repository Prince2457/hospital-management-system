from utils.doctors import get_all_doctors, create_doctor
from utils.appointments import get_all_appointments, create_appointment

create_appointment(2, 1, '2026-03-15', '10:00:00', 'scheduled', 'First consultation')

appointments = get_all_appointments()
print(f"\nAll appointments ({len(appointments)} found):")
for appointment in appointments:
    print(f"{appointment['appointment_id']} - {appointment['patient_id']} - {appointment['status']}")