from utils.db_helpers import execute_query
def get_all_billing():
    return execute_query("SELECT * FROM billing", fetch="all") or []

def get_billing_by_id(bill_id):
    return execute_query("SELECT * FROM billing WHERE bill_id =%s",(bill_id,), fetch="one")

def create_bill(patient_id, appointment_id, bill_item, amount, payment_status, payment_date):
    return execute_query("""INSERT INTO billing (patient_id, appointment_id, bill_item, amount, payment_status, payment_date) 
                    VALUES(%s,%s,%s,%s,%s,%s)""",
                    (patient_id, appointment_id, bill_item, amount, payment_status, payment_date),
                    commit=True)

def update_bill(bill_id, patient_id, appointment_id, bill_item, amount, payment_status, payment_date):
    return execute_query(
        """UPDATE billing SET
        patient_id=%s,
        appointment_id=%s,
        bill_item=%s,
        amount=%s,
        payment_status=%s,
        payment_date=%s,
        WHERE bill_id =%s
        """,(patient_id, appointment_id, bill_item, amount, payment_status, payment_date,bill_id),
        commit=True
    )

def delete_bill(bill_id):
    return execute_query("DELETE FROM billing WHERE bill_id=%s",(bill_id,), commit=True)
    
