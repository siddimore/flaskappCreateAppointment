"""
Flask API

"""

from controller.controller import AppointmentController
from flask import Flask, request, jsonify
from middleware import middleware

app = Flask(__name__)


# calling our middleware
# app.wsgi_app = middleware(app.wsgi_app)

@app.route("/api", methods=['GET', 'POST'])
def appoiintment_schedduler():
    # API Keys
    API_METHOD = "method"

    # API Methods
    CREATE_APPOINTMENT = "create_appointment"
    GET_APPOINTMENTS = "get_appointments"
    UPDATE_APPOINTMENT = "update_appointment"
    DELETE_APPOINTMENT = "delete_appointment"

    # API Parameters
    DOCTOR_ID = "doctor_id"
    PATIENT_NAME = "patient_name"
    APPOINTMENT_ID = "appointment_id"
    APPOINTMENT_DESCRIPTION = "appointment_description"
    APPOINTMENT_START_TIME = "appointment_start_time"
    APPOINTMENT_END_TIME = "appointment_end_time"

    MESSAGE_ERROR_INVALID_METHOD = "{'error': 'Invalid method'}"

    response = MESSAGE_ERROR_INVALID_METHOD

    appointment_controller = AppointmentController()

    api_method = request.args.get(API_METHOD)
    
    if api_method == CREATE_APPOINTMENT:
        doctor_id = request.args.get(DOCTOR_ID)
        patient_name = request.args.get(PATIENT_NAME)
        description = request.args.get(APPOINTMENT_DESCRIPTION)
        appt_start = request.args.get(APPOINTMENT_START_TIME)
        appt_end = request.args.get(APPOINTMENT_END_TIME)

        response = appointment_controller.create(doctor_id, patient_name, description, appt_start, appt_end)

    elif api_method == GET_APPOINTMENTS:
        appointment_id = request.args.get(APPOINTMENT_ID)
        response = appointment_controller.get_appt_by_id(appointment_id)

    elif api_method == UPDATE_APPOINTMENT:
        doctor_id = request.args.get(DOCTOR_ID)
        appointment_id = request.args.get(APPOINTMENT_ID)
        description = request.args.get(APPOINTMENT_DESCRIPTION)
        appt_start = request.args.get(APPOINTMENT_START_TIME)
        appt_end = request.args.get(APPOINTMENT_END_TIME)
        response = appointment_controller.update(doctor_id, patient_name, description, appt_start, appt_end, appointment_id)
    
    elif api_method == DELETE_APPOINTMENT:
        appointment_id = request.args.get(APPOINTMENT_ID)
        response = appointment_controller.delete(appointment_id)

    if response is None:
        return "Bad Request", 404
    return jsonify(response), 200

if __name__ == "__main__":
    app.run()

