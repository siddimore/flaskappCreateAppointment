
import uuid

class Doctor:
    def __init__(self, doctor_id:str, doctor_name: str, field: str) -> None:
        self.id = str(uuid.uuid4()) if doctor_id else ""
        self.doctor_name = doctor_name if doctor_name else ""
        self.field = field if field else ""