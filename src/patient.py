"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""
import uuid
import datetime
from api_controller import commit_patient as commit_to_database
from config import config_data as app_config
from db_config import db_data as database_config

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = name
        self.patient_gender = gender
        self.patient_age = age
        self.patient_checkin = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.patient_checkout = None
        self.patient_room = None
        self.patient_ward = None

    def update_room_and_ward(self, room, ward):
        if room in app_config['ROOM_NUMBERS'] and ward in app_config['WARD_NUMBERS']:
            self.patient_room = room
            self.patient_ward = ward
            message = "Room and ward updated successfully."
        else:
            message = "Invalid room or ward."
        return message

    def commit_to_database(self):
        validation_failed = False
        # Perform validation
        for attr, value in self.__dict__.items():
            if attr in database_config and value is not None and value not in database_config[attr]:
                print(f"Validation failed for {attr}: {value}")
                validation_failed = True
                break
        
        if not validation_failed:
            # Commit patient to the database using the API controller
            commit_to_database(self.__dict__)
            message = "Patient committed to the database."
        else:
            message = "Failed to commit patient to the database due to validation error."
        return message
