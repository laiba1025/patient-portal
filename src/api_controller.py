from flask import Flask, request, jsonify
from patient_db import PatientDB

class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        self.app.route("/patients", methods=["GET"])(self.list_patients)
        self.app.route("/patients/<patient_name>", methods=["GET"])(self.list_patient_by_name)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_certain_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)

    def list_patients(self):
        try:
            patients_data = self.patient_db.select_all_patients()
            if patients_data is not None:
                return jsonify({"patients": patients_data}), 200
            else:
                return jsonify({"error": "Failed to retrieve patients"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    def list_patient_by_name(self, patient_name):
        try:
            matching_patients = self.patient_db.fetch_patient_id_by_name(patient_name)
            if matching_patients is not None:
                return jsonify({"matching_patients": matching_patients}), 200
            else:
                return jsonify({"error": "No patients found with the given name"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    def get_certain_patient(self, patient_id):
        try:
            selected_patient = self.patient_db.select_patient(patient_id)
            if selected_patient is not None:
                return jsonify({"selected_patient": selected_patient}), 200
            else:
                return jsonify({"error": "Patient not found"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400
        
    def create_patient(self):
        try:
            request_data = request.json
            inserted_patient_id = self.patient_db.insert_patient(request_data)
            if inserted_patient_id:
                return jsonify({"inserted_patient_id": inserted_patient_id[0]}), 200
            else:
                return jsonify({"error": "Failed to insert patient"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400
        

    def update_patient(self, patient_id):
        try:
            request_data = request.json
            num_updated_rows = self.patient_db.update_patient(patient_id, request_data)
            if num_updated_rows is not None:
                return jsonify({"num_updated_rows": num_updated_rows}), 200
            else:
                return jsonify({"error": "Failed to update patient"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    def delete_patient(self, patient_id):
        try:
            num_deleted_rows = self.patient_db.delete_patient(patient_id)
            if num_deleted_rows is not None:
                return jsonify({"num_deleted_rows": num_deleted_rows}), 200
            else:
                return jsonify({"error": "Failed to delete patient"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    def run(self):
        self.app.run()

PatientAPIController()
