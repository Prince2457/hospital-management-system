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
        payment_date=%s
        WHERE bill_id =%s
        """,(patient_id, appointment_id, bill_item, amount, payment_status, payment_date,bill_id),
        commit=True
    )

def delete_bill(bill_id):
    return execute_query("DELETE FROM billing WHERE bill_id=%s",(bill_id,), commit=True)
    
def mark_bill_paid(bill_id):
    existing = execute_query(
        "SELECT * FROM  billing WHERE bill_id =%s",
        (bill_id,), fetch="one"
    )
    if not existing:
        return "not found"
    if existing['payment_status'] == 'paid':
        return "already paid"
    return execute_query(
        """UPDATE billing SET
        payment_status = 'paid',
        payment_date = CURDATE()
        WHERE bill_id =%s""", (bill_id,), commit=True
    )

def get_outstanding_bill():
    return execute_query(
        """SELECT * FROM billing
        WHERE payment_status IN ('pending', 'overdue')
        ORDER BY created_at ASC""",fetch="all"
    ) or []

def get_financial_summary():
    return execute_query(
        """SELECT
        COUNT(*) as total_bills,
        SUM(CASE WHEN payment_status = 'paid'
            THEN amount ELSE 0 END) as total_revenue,
        SUM(CASE WHEN payment_status = 'pending'
            THEN amount ELSE 0 END) as total_pending,
        SUM(CASE WHEN payment_status = 'overdue'
            THEN amount ELSE 0 END) as total_overdue,
        COUNT(CASE WHEN payment_status = 'paid'
            THEN 1 END) as paid_count,
        COUNT(CASE WHEN payment_status = 'pendin'
            THEN 1 END) as pending_count
        FROM billing""", fetch="one"
    )

def flag_overdue_bills():
    return execute_query(
        """UPDATE billing
        SET payment_status = 'overdue' 
        WHERE payment_status = 'pending'
        AND DATEDIFF(CURDATE(), created_at) > 7""",
        commit=True
    )