import uuid
import datetime

class Appointment:
    def __init__(self, doctor_id: str, patient_name: str, doctor_name: str, description: str, appt_start: datetime, appt_end: datetime, appointment_id: str) -> None:
        self.id = appointment_id if appointment_id else str(uuid.uuid4())
        self.doctor_id = doctor_id
        self.patient_name = patient_name if patient_name else ""
        self.doctor_name = doctor_name if doctor_name else ""
        self.description = description if description else ""
        self.appt_start = appt_start 
        self.appt_end = appt_end

    def get_item_as_dict(self) -> dict:
        return {"patient_name": self.patient_name, "doctor_name": self.doctor_name, "description": self.description, "appt_start": self.appt_start, "appt_end": self.appt_end,  "appointment_id": self.id}
