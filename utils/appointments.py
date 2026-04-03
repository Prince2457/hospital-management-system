
from utils.db_helpers import execute_query

def get_all_appointments():
    """Fetch all appontments from database .Return a list of dictionary."""
    return execute_query(query="SELECT * FROM appointments", fetch="all") or []


def get_appointment_by_id(appointment_id):
    """Fectch an appointment from database using the primary key appoinment."""
    return execute_query('SELECT * FROM appointments WHERE appointment_id =%s',(appointment_id,), fetch="one" )


def create_appointment(patient_id, doctor_id, appointment_date, appointment_time, status, notes):
    """Insert into database to create an appointment."""
    return execute_query("""INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
                        VALUES (%s,%s,%s,%s,%s,%s)""",(patient_id, doctor_id, appointment_date, appointment_time, status, notes),
                        commit=True)


def update_appointment(appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, notes):
    """Update set appointment in the database."""
    return execute_query("""UPDATE appointments SET
                        patient_id=%s,
                        doctor_id=%s,
                        appointment_date=%s,
                        appointment_time=%s,
                        status=%s,
                        notes=%s
                        WHERE appointment_id =%s""",
                        (patient_id, doctor_id, appointment_date, appointment_time, status, notes, appointment_id),
                        commit=True)


def delete_appointment(appointment_id): 
    """Delete appointment from the database ."""   
    return execute_query('DELETE  FROM appointments WHERE appointment_id =%s',(appointment_id,), commit=True )

def check_doctor_availability(doctor_id, appointment_date, appointment_time):
    """Checking doctor availability of doctor by feching appointment date, appointment time and status if scheduled for a particular doctor. """
    result = execute_query(
        """SELECT * FROM appointments
        WHERE doctor_id = %s
        AND appointment_date = %s
        AND appointment_time =%s
        AND status = 'scheduled'""",
        (doctor_id, appointment_date, appointment_time),
        fetch="one"
    )
    return result is None

def cancel_appointment(appointment_id):
    """Cancel appointment """
    return execute_query(
        """UPDATE appointments
        SET status = 'cancelled'
        WHERE appointment_id =%s
        AND status = 'scheduled'""",
        (appointment_id,), commit=True
    )

def get_patient_appointments(patient_id):
    """Feching patient appointment history."""
    return execute_query(
        """SELECT a.appointment_id, a.appointment_date,
        a.appointment_time, a.status, a.notes,
        d.specialization, d.department
        FROM appointments a
        JOIN doctors d ON  a.doctor_id = d.doctor_id 
        WHERE a.patient_id =%s
        ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
        (patient_id,), 
        fetch= "all"
    ) or []  

def generate_bill_from_appointment(appointment_id):
    """Fetch from appoitment to insert billing in the database to create a bill."""
    appointment = execute_query(
        """SELECT a.appointment_id, a.patient_id,
        a.doctor_id, d.consultation_fee
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE appointment_id =%s""",(appointment_id,), fetch="one"
    )    
    if not appointment:
        return "not found"
    return execute_query(
        """INSERT INTO BILLING 
        (patient_id, appointment_id, bill_item, amount, payment_status)
        VALUES (%s,%s,%s,%s,'pending')""",
        (appointment['patient_id'],appointment['appointment_id'],'consultation_fee', appointment['consultation_fee']), commit=True)
