class MedicalRecords:
    def __init__(self, record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment=None, lab_test=None, notes=None):

        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_id = appointment_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.lab_test = lab_test
        self.notes = notes

    def __str__(self):
        return f"Record({self.record_id}) - Patient({self.patient_id}) | DR.({self.doctor_id}) | {self.diagnosis} | {self.treatment} | {self.notes}"     
        