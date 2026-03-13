class Doctor:
    def __init__(self, doctor_id, full_name, license_number, 
                specialization=None, available_days=None,
                consultation_fee=0.00):
        
        self.doctor_id = doctor_id
        self.full_name = full_name
        self.license_number = license_number
        self.specialization = specialization
        self.available_days = available_days
        self.consultation_fee = consultation_fee

    def __str__(self):
        return f"Doctor({self.doctor_id}) - Dr. {self.full_name} | {self.specialization}"      