import csv
import os
from utils.db_helpers import execute_query

def get_financial_report(start_date=None, end_date=None):
    """Fetch bill report"""
    query = """
        SELECT b.bill_id, p.full_name, b.bill_item,
        b.amount, b.payment_status, b.payment_date,
        b.created_at
        FROM billing b
        JOIN patients p ON b.patient_id = p.patient_id
        ORDER BY b.created_at DESC
    """
    return execute_query(query, fetch="all") or []

def get_appointment_report():
    """Fetch  appoinment report"""
    return execute_query(
        """ SELECT a.appointment_id, p.full_name as patient_name,
        d.specialization, d.department,
        a.appointment_date, a.appointment_time, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC """,
        fetch="all"
    ) or []

def get_patient_report():
    """Fetch patient report."""
    return execute_query(
        """SELECT patient_id, full_name, ghana_card_number,
        gender, phone, region, blood_group, registered_at
        FROM patients
        ORDER BY registered_at DESC""",
        fetch="all"
    ) or []

def export_to_csv(data, filename, folder="reports"):
    """Make a new csv file called reports"""
    if not data:
        return None
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename) 

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return filepath      