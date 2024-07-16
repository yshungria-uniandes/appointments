from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime

DB_NAME = 'appointments_schema'

class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data.get('updated_at')
        self.user_id = data['user_id']

    @classmethod
    def create_new_appointment(cls, data):
        query = '''
                INSERT INTO appointments (task, status, created_at, user_id)
                VALUES (%(task)s, %(status)s, %(created_at)s, %(user_id)s);
                '''
        response_query = connectToMySQL(DB_NAME).query_db(query, data)
        return response_query

    @classmethod
    def get_all_appointments(cls):
        query = '''
                SELECT * FROM appointments
                '''
        response_query_appointments = connectToMySQL(DB_NAME).query_db(query)
        appointments = [cls(appointment) for appointment in response_query_appointments]
        return appointments

    @classmethod
    def get_all_appointments_by_id(cls, data):
        query = '''
                SELECT * FROM appointments WHERE user_id = %(id)s;
                '''
        response_query_appointments = connectToMySQL(DB_NAME).query_db(query, data)
        appointments = [cls(appointment) for appointment in response_query_appointments]
        return appointments

    @classmethod
    def get_appointment_by_id(cls, data):
        query = '''
                SELECT * FROM appointments WHERE id = %(id)s;
                '''
        response_query_appointment = connectToMySQL(DB_NAME).query_db(query, data)
        return cls(response_query_appointment[0]) if response_query_appointment else None

    @classmethod
    def update_appointment_by_id(cls, data):
        query = '''
                UPDATE appointments
                SET task=%(task)s, status=%(status)s, updated_at=NOW()
                WHERE id=%(id)s;
                '''
        response_query_update = connectToMySQL(DB_NAME).query_db(query, data)
        return response_query_update

    @classmethod
    def delete_appointment_by_id(cls, data):
        query = '''
                DELETE FROM appointments WHERE id=%(id)s;
                '''
        response_query_delete = connectToMySQL(DB_NAME).query_db(query, data)
        return response_query_delete

    @staticmethod
    def validate_appointment_form(data):
        if len(data['task']) < 3:
            flash("La tarea necesita al menos 3 caracteres", "create")
            return False
        if not data['date']:
            flash("Necesita agregar una fecha", "create")
            return False
        return True

    @staticmethod
    def validate_user_appointment(data, id):
        all_appointments = Appointment.get_all_appointments_by_id(data)
        count = sum(1 for appointment in all_appointments if appointment.id == id)
        return count == 1
