from utils.db_helpers import execute_query

def get_all_patients():
    """Fetch all patient from the database.Returns a list of dictionary"""
    return execute_query("SELECT * FROM patients", fetch="all") or []

def get_patient_by_id(patient_id):
    """Fetch a patient from the databse using a patient_id which is the unique key."""
    return execute_query("SELECT  * FROM patients WHERE patient_id =%s",(patient_id,), fetch="one")

def create_patient(full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by): 
    """Insert into database to create a patient"""
    return execute_query("""INSERT INTO patients (full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (full_name, ghana_card_number, date_of_birth, gender,
                phone, email, address, region, blood_group,
                nhis_number, nhis_expiry, emergency_contact_name,
                emergency_contact_phone, registered_by), commit= True)

def update_patient(patient_id, full_name, phone, email, address, region, 
                blood_group, nhis_number, nhis_expiry, 
                emergency_contact_name, emergency_contact_phone):
    """Update  details of patients in database."""
    return execute_query("""
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
            patient_id), commit=True)


def delete_patient(patient_id):
    """Delete patient from database ."""
    return execute_query("DELETE FROM patients WHERE patient_id = %s",(patient_id,), commit=True) 