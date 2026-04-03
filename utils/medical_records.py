from utils.db_helpers import execute_query

def get_all_medical_records():
    """Fetch all medical records from database.Return a list of dictionary"""
    return execute_query("SELECT * FROM  medical_records", fetch="all") or []


def get_medical_record_by_id(record_id):
    """Fetch medical records from database using record_id"""
    return execute_query("SELECT * FROM medical_records WHERE record_id=%s",(record_id,), fetch="one")


def create_record(patient_id, doctor_id, appointment_id, diagnosis, treatment, lab_tests, notes):
    """Insert into database to create a medical records of a patient."""
    return execute_query("""INSERT INTO medical_records (patient_id, doctor_id, appointment_id, diagnosis, treatment, lab_tests, notes)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (patient_id, doctor_id, appointment_id, diagnosis, treatment, lab_tests, notes),
                        commit=True)


def update_medical_record(record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, lab_tests, notes):
    """Update medical records."""
    return execute_query(
        """ UPDATE medical_records SET
        patient_id=%s,
        doctor_id=%s,
        appointment_id=%s,
        diagnosis=%s,
        treatment=%s,
        lab_tests=%s,
        notes=%s
        WHERE record_id=%s""",
        (patient_id, doctor_id, appointment_id, diagnosis, treatment, lab_tests, notes, record_id), commit=True)

def delete_medical_record(record_id):
    """Delete medical records from the database."""
    return execute_query("DELETE FROM medical_records WHERE record_id=%s",(record_id,), commit=True)    