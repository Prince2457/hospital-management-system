from config.db import get_connection, close_connection
from utils.patients import get_all_patients
def main():
    print("🏥 Hospital Management System")
    print("=" * 40)

    patients = get_all_patients()

    if patients:
        print(f"Found {len(patients)} patients:")
        for patient in patients:
            print(patient)

    else:
        print("NO patients found")    
    
    

if __name__ == "__main__":
    main()