
from dao.comsos_db_sql import CosmosSQL
from flask import jsonify
from model.appointment import Appointment
import datetime

class AppointmentController:
    def __init__(self) -> None:
        self.appointment_dao = CosmosSQL()

    def create(self, doctor_id: str, patient_name: str, doctor_name: str, description: str, appt_start: datetime, appt_end: datetime) -> None: 
        appointment = Appointment(doctor_id, patient_name, description, appt_start, appt_end).get_item_as_dict()
        return self.appointment_dao.create_item(appointment)


    def delete(self, appointment_id: str) -> bool:
        return self.appointment_dao.delete_item(appointment_id)


    def get_appt_by_id(self, appointment_id: str) -> Appointment:
        return self.appointment_dao.read_item_by_partition_key(appointment_id)


    def get_appointments(self) -> list[Appointment]:
        return self.appointment_dao.read_items()


    def update(self, doctor_id: str, patient_name: str, doctor_name: str, description: str, appt_start: datetime, appt_end: datetime, appointment_id: str) -> Appointment:

        item_body = Appointment(doctor_id, patient_name, description, appt_start, appt_end, appointment_id).get_item_as_dict()
        # identify and discard properties without a value to update
        items_to_discard = []
        for property, value in item_body.items():
            if not value:
                items_to_discard.append(property)
        for item in items_to_discard:
            del item_body[item]


        return self.appointment_dao.update_item(appointment_id, item_body)
