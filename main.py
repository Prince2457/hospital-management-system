from config.db import get_connection, close_connection
from utils.patients import get_all_patients, get_patient_by_id ,create_patient,update_patient,delete_patient
def main():
    print("🏥 Hospital Management System")
    print("=" * 40)
    delete_patient(3)
    patients = get_all_patients()
    for patient in patients:
        print(patient['patient_id'], '-', patient['full_name'])
    


if __name__ == "__main__":
    main()