class Billing:
    def __init__(self, bill_id, patient_id, appointment_id, bill_item, amount=0.00, payment_status="pending", payment_date=None):

        self.bill_id = bill_id
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.bill_item = bill_item
        self.amount = amount
        self.payment_status = payment_status
        self.payment_date = payment_date

    def __str__(self):
        return (f"Bill({self.bill_id}) - Patient({self.patient_id}) | Appointment({self.appointment_id}) | {self.bill_item} | {self.amount} | {self.payment_status}")     