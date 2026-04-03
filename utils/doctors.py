from utils.db_helpers import execute_query

def get_all_doctors():
    """Fectch all doctors from database.Return a list of dictionary. """
    return execute_query("SELECT * FROM doctors") or []

def get_doctor_by_id(doctor_id):
    """Fetch doctor from database using doctor_id as the primary key. """
    return execute_query("SELECT * FROM doctors WHERE doctor_id =%s",(doctor_id,), fetch="one")

def create_doctor(user_id, specialization, qualification, license_number, department, available_days, consultation_fee):
    """Insert into database to create a doctor."""
    return execute_query(
        """INSERT INTO doctors 
                (user_id, specialization, qualification, license_number, department, available_days, consultation_fee) 
                VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                    (user_id, specialization, qualification, license_number, department, available_days, consultation_fee ), commit=True)
    

def update_doctor(doctor_id, user_id, specialization, qualification, license_number, department, available_days, consultation_fee):
    """Update doctor details in the database."""
    return execute_query(
        """UPDATE doctors SET
            user_id =%s,
            specialization=%s,
            qualification=%s,
            license_number=%s,
            department=%s,
            available_days=%s,
            consultation_fee=%s
            WHERE doctor_id =%s
        """,
        (user_id, specialization, qualification, license_number, department, available_days, consultation_fee, doctor_id), commit=True
    )

def delete_doctor(doctor_id):
    """Delete doctor details from the details ."""
    return execute_query("DELETE FROM doctors WHERE doctor_id =%s",(doctor_id,), commit=True)