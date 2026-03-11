from config.db import get_connection
from config.db import close_connection

def get_all_patients():
    connection = get_connection()
    
    if not connection :
        return []
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        return patients
    
    except Exception as e:
        print(f"❌ Error fetching patients: {e}")
        return []
    finally:
        close_connection(connection, cursor)  

def get_patient_by_id(patient_id):
    connection = get_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM patients WHERE patient_id =%s",(patient_id,))
        patient = cursor.fetchone()
        return patient
    except Exception as e:
        print(f"❌ Error fetching patient: {e}")
        return None
    finally:
        close_connection(connection, cursor)

def create_patient(full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by): 
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()

    try:
        cursor.execute("""INSERT INTO patients (full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by))
        
        connection.commit()
        print(f"✅ Patient {full_name} created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating patient: {e}")
        connection.rollback()
        return False
    finally:
        close_connection(connection, cursor)

def update_patient(patient_id, full_name, phone, email, address, region, 
                blood_group, nhis_number, nhis_expiry, 
                emergency_contact_name, emergency_contact_phone):
    """Update an existing patient's details."""
    connection = get_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE patients SET
                full_name = %s,
                phone = %s,
                email = %s,
                address = %s,
                region = %s,
                blood_group = %s,
                nhis_number = %s,
                nhis_expiry = %s,
                emergency_contact_name = %s,
                emergency_contact_phone = %s
            WHERE patient_id = %s
        """, (full_name, phone, email, address, region,
            blood_group, nhis_number, nhis_expiry,
            emergency_contact_name, emergency_contact_phone,
            patient_id))

        connection.commit()
        print(f"✅ Patient {patient_id} updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error updating patient: {e}")
        connection.rollback()
        return False 
    finally:
        close_connection(connection, cursor)     

def delete_patient(patient_id):
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM patients WHERE patient_id = %s",(patient_id,))

        connection.commit()
        if cursor.rowcount == 0:
            print(f"❌ Patient {patient_id} not found.")
            return False

        print(f"✅ Patient {patient_id} deleted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error deleting patient: {e}")
        connection.rollback()
        return False
    finally:
        close_connection(connection, cursor)