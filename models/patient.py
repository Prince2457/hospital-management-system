class Patient:
    def __init__(self, patient_id, full_name, ghana_card_number,
                date_of_birth, gender, phone, email=None,
                address=None, blood_group=None):
        
        self.patient_id = patient_id
        self.full_name = full_name
        self.ghana_card_number = ghana_card_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.blood_group = blood_group

    def __str__(self):
        return f"Patient({self.patient_id}) - {self.full_name} | {self.phone}" 