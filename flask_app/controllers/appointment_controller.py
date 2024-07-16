from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.appointment_model import Appointment

@app.route("/appointments/new", methods=['GET', 'POST'])
def create_appointment():
    if request.method == 'GET':    
        if 'id' not in session:
            return redirect('/logout')
        return render_template("create_appointment.html")
    elif request.method == 'POST':
        if not Appointment.validate_appointment_form(request.form):
            return redirect("/appointments/new")
        data = {
            'task': request.form['task'],
            'status': request.form['status'],
            'created_at': request.form['date'],
            'user_id': session['id']
        }    
        creating_appointment = Appointment.create_new_appointment(data)
        print("new appointment created", creating_appointment)
        return redirect("/dashboard")

@app.route("/appointments/<int:id>", methods=['GET'])
def read_appointment(id):
  
    appointment = Appointment.get_appointment_by_id({"id": id})
    
    return render_template('read_appointment.html', appointment=appointment)

@app.route("/appointments/edit/<int:id>", methods=['GET', 'POST'])
def edit_appointment(id):
    if request.method == 'GET':
        data_id = {
            "id": session.get('id')
        }
        if not Appointment.validate_user_appointment(data_id, id):
            return redirect("/danger")

        data = {
            'id': id
        }
        appointment = Appointment.get_appointment_by_id(data)
        appointment.created_at = appointment.created_at.strftime("%Y-%m-%d")
        return render_template("edit_appointment.html", appointment=appointment)
    
    elif request.method == 'POST':
        if not Appointment.validate_appointment_form(request.form):
            return redirect(f"/appointments/edit/{id}")
        data = {
            'task': request.form['task'],
            'status': request.form['status'],
            'created_at': request.form['date'],
            'id': id
        }
        resultado = Appointment.update_appointment_by_id(data)
        print(resultado)
        return redirect("/dashboard")

@app.route("/appointments/delete/<int:id>")
def delete_appointment(id):
    if 'id' not in session:
        return redirect('/logout')
    data_id = {
        "id": session.get('id')
    }
    if not Appointment.validate_user_appointment(data_id, id):
        return redirect("/danger")
    data = {
        'id': id
    }
    print("aqui id para eliminar", id)
    print(Appointment.delete_appointment_by_id(data))    
    return redirect("/dashboard")

from flask_app.models.appointment_model import Appointment

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if 'id' not in session:
        return redirect('/logout')
    
    data = {
        "id": session.get('id')
    }

    current_appointments = Appointment.get_all_appointments_by_id(data)
    past_appointments = [appointment for appointment in current_appointments if appointment.status != 'Pending']
    current_appointments = [appointment for appointment in current_appointments if appointment.status == 'Pending']
    
    return render_template("dashboard.html", appointments=current_appointments, past_appointments=past_appointments)
