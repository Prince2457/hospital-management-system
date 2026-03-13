class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id,
                appointment_date, appointment_time,
                status="scheduled", notes=None):
        
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.notes = notes

    def __str__(self):
        return f"Appointment({self.appointment_id}) - Patient({self.patient_id}) | Dr.{self.doctor_id} | {self.appointment_date} | {self.status}"    