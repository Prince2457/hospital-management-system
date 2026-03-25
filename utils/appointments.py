
from utils.db_helpers import execute_query

def get_all_appointments():
    return execute_query(query="SELECT * FROM appointments", fetch="all") or []


def get_appointment_by_id(appointment_id):
    return execute_query('SELECT * FROM appointments WHERE appointment_id =%s',(appointment_id,), fetch="one" )


def create_appointment(patient_id, doctor_id, appointment_date, appointment_time, status, notes):
    return execute_query("""INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
                        VALUES (%s,%s,%s,%s,%s,%s)""",(patient_id, doctor_id, appointment_date, appointment_time, status, notes),
                        commit=True)


def update_appointment(appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, notes):
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
    return execute_query('DELETE  FROM appointments WHERE appointment_id =%s',(appointment_id,), commit=True )

def check_doctor_availability(doctor_id, appointment_date, appointment_time):
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
    return execute_query(
        """UPDATE appointments
        SET status = 'cancelled'
        WHERE appointment_id =%s
        AND status = 'scheduled'""",
        (appointment_id,), commit=True
    )

def get_patient_appointments(patient_id):
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
