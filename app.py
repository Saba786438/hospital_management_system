from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from itertools import count

app = Flask(__name__)
app.secret_key = "change-this-development-secret"

# In-memory sample data only. Changes disappear when the server restarts.
patients = [
    {"id": 1001, "name": "Aarav Sharma", "age": 34, "gender": "Male", "phone": "9876543210", "email": "aarav@example.com", "condition": "Routine check-up"},
    {"id": 1002, "name": "Priya Nair", "age": 28, "gender": "Female", "phone": "9876501234", "email": "priya@example.com", "condition": "Migraine"},
    {"id": 1003, "name": "Rahul Verma", "age": 52, "gender": "Male", "phone": "9876512345", "email": "rahul@example.com", "condition": "Blood pressure review"},
]
doctors = [
    {"id": 201, "name": "Dr. Meera Iyer", "specialty": "Cardiology", "phone": "9000011111", "email": "meera@careplus.demo", "availability": "Mon–Fri"},
    {"id": 202, "name": "Dr. Arjun Rao", "specialty": "Neurology", "phone": "9000022222", "email": "arjun@careplus.demo", "availability": "Tue–Sat"},
    {"id": 203, "name": "Dr. Sara Khan", "specialty": "Pediatrics", "phone": "9000033333", "email": "sara@careplus.demo", "availability": "Mon–Sat"},
    {"id": 204, "name": "Dr. Karthik Menon", "specialty": "Orthopedics", "phone": "9000044444", "email": "karthik@careplus.demo", "availability": "Mon–Thu"},
]
appointments = [
    {"id": 301, "patient_id": 1001, "patient": "Aarav Sharma", "doctor_id": 201, "doctor": "Dr. Meera Iyer", "date": date.today().isoformat(), "time": "09:30", "reason": "Routine check-up", "status": "Confirmed"},
    {"id": 302, "patient_id": 1002, "patient": "Priya Nair", "doctor_id": 202, "doctor": "Dr. Arjun Rao", "date": date.today().isoformat(), "time": "11:00", "reason": "Recurring headache", "status": "Waiting"},
    {"id": 303, "patient_id": 1003, "patient": "Rahul Verma", "doctor_id": 201, "doctor": "Dr. Meera Iyer", "date": date.today().isoformat(), "time": "14:00", "reason": "BP follow-up", "status": "Completed"},
]
bills = [
    {"id": 401, "patient_id": 1001, "patient": "Aarav Sharma", "description": "Consultation", "amount": 800.0, "date": date.today().isoformat(), "status": "Paid"},
    {"id": 402, "patient_id": 1002, "patient": "Priya Nair", "description": "Neurology consultation", "amount": 1200.0, "date": date.today().isoformat(), "status": "Pending"},
    {"id": 403, "patient_id": 1003, "patient": "Rahul Verma", "description": "Consultation + tests", "amount": 1850.0, "date": date.today().isoformat(), "status": "Paid"},
]
patient_ids = count(1004)
doctor_ids = count(205)
appointment_ids = count(304)
bill_ids = count(404)

def money(value):
    return f"₹{value:,.2f}"

app.jinja_env.filters["money"] = money

@app.route("/")
def dashboard():
    today = date.today().isoformat()
    todays_appointments = [a for a in appointments if a["date"] == today]
    paid_revenue = sum(b["amount"] for b in bills if b["status"] == "Paid")
    pending_amount = sum(b["amount"] for b in bills if b["status"] == "Pending")
    upcoming = sorted(appointments, key=lambda a: (a["date"], a["time"]))[:5]
    return render_template("dashboard.html", patients=patients, doctors=doctors,
                           appointments=appointments, bills=bills,
                           todays_appointments=todays_appointments,
                           paid_revenue=paid_revenue, pending_amount=pending_amount,
                           upcoming=upcoming, today=today, active="dashboard")

@app.route("/patients", methods=["GET", "POST"])
def patient_list():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        phone = request.form.get("phone", "").strip()
        gender = request.form.get("gender", "").strip()
        if not name or not age_text.isdigit() or int(age_text) < 0 or not phone or not gender:
            flash("Please enter a valid name, age, phone number, and gender.", "error")
            return redirect(url_for("patient_list"))
        patients.append({"id": next(patient_ids), "name": name, "age": int(age_text),
                         "gender": gender, "phone": phone,
                         "email": request.form.get("email", "").strip(),
                         "condition": request.form.get("condition", "").strip() or "Not specified"})
        flash(f"Patient {name} registered successfully.", "success")
        return redirect(url_for("patient_list"))
    q = request.args.get("q", "").strip().lower()
    filtered = [p for p in patients if q in " ".join(str(v) for v in p.values()).lower()]
    return render_template("patients.html", patients=filtered, active="patients", q=q)

@app.route("/doctors", methods=["GET", "POST"])
def doctor_list():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        specialty = request.form.get("specialty", "").strip()
        phone = request.form.get("phone", "").strip()
        if not name or not specialty or not phone:
            flash("Doctor name, specialty, and phone are required.", "error")
            return redirect(url_for("doctor_list"))
        doctors.append({"id": next(doctor_ids), "name": name, "specialty": specialty,
                        "phone": phone, "email": request.form.get("email", "").strip(),
                        "availability": request.form.get("availability", "").strip() or "By appointment"})
        flash(f"{name} added to the doctor directory.", "success")
        return redirect(url_for("doctor_list"))
    q = request.args.get("q", "").strip().lower()
    filtered = [d for d in doctors if q in " ".join(str(v) for v in d.values()).lower()]
    return render_template("doctors.html", doctors=filtered, active="doctors", q=q)

@app.route("/appointments", methods=["GET", "POST"])
def appointment_list():
    if request.method == "POST":
        patient_id = request.form.get("patient_id", type=int)
        doctor_id = request.form.get("doctor_id", type=int)
        appt_date = request.form.get("date", "")
        appt_time = request.form.get("time", "")
        reason = request.form.get("reason", "").strip()
        patient = next((p for p in patients if p["id"] == patient_id), None)
        doctor = next((d for d in doctors if d["id"] == doctor_id), None)
        try:
            datetime.strptime(appt_date, "%Y-%m-%d")
            datetime.strptime(appt_time, "%H:%M")
            valid_date = appt_date >= date.today().isoformat()
        except ValueError:
            valid_date = False
        if not patient or not doctor or not valid_date or not reason:
            flash("Please choose a patient and doctor, a valid future date/time, and enter a reason.", "error")
            return redirect(url_for("appointment_list"))
        conflict = any(a["doctor_id"] == doctor_id and a["date"] == appt_date and a["time"] == appt_time and a["status"] != "Cancelled" for a in appointments)
        if conflict:
            flash("That doctor already has an appointment at this date and time.", "error")
            return redirect(url_for("appointment_list"))
        appointments.append({"id": next(appointment_ids), "patient_id": patient_id,
                             "patient": patient["name"], "doctor_id": doctor_id,
                             "doctor": doctor["name"], "date": appt_date, "time": appt_time,
                             "reason": reason, "status": "Confirmed"})
        flash("Appointment booked successfully.", "success")
        return redirect(url_for("appointment_list"))
    q = request.args.get("q", "").strip().lower()
    filtered = [a for a in appointments if q in " ".join(str(v) for v in a.values()).lower()]
    return render_template("appointments.html", appointments=sorted(filtered, key=lambda a: (a["date"], a["time"])),
                           patients=patients, doctors=doctors, active="appointments", q=q, today=date.today().isoformat())

@app.post("/appointments/<int:appointment_id>/status")
def appointment_status(appointment_id):
    appointment = next((a for a in appointments if a["id"] == appointment_id), None)
    status = request.form.get("status", "")
    if appointment and status in {"Confirmed", "Waiting", "Completed", "Cancelled"}:
        appointment["status"] = status
        flash("Appointment status updated.", "success")
    return redirect(request.referrer or url_for("appointment_list"))

@app.route("/billing", methods=["GET", "POST"])
def billing():
    if request.method == "POST":
        patient_id = request.form.get("patient_id", type=int)
        patient = next((p for p in patients if p["id"] == patient_id), None)
        description = request.form.get("description", "").strip()
        amount_text = request.form.get("amount", "").strip()
        try:
            amount = float(amount_text)
            valid_amount = amount > 0
        except ValueError:
            valid_amount = False
            amount = 0
        if not patient or not description or not valid_amount:
            flash("Choose a patient and enter a description and a positive amount.", "error")
            return redirect(url_for("billing"))
        bills.append({"id": next(bill_ids), "patient_id": patient_id, "patient": patient["name"],
                      "description": description, "amount": amount,
                      "date": date.today().isoformat(), "status": "Pending"})
        flash("Bill created successfully.", "success")
        return redirect(url_for("billing"))
    q = request.args.get("q", "").strip().lower()
    filtered = [b for b in bills if q in " ".join(str(v) for v in b.values()).lower()]
    return render_template("billing.html", bills=filtered, patients=patients, active="billing", q=q)

@app.post("/billing/<int:bill_id>/pay")
def pay_bill(bill_id):
    bill = next((b for b in bills if b["id"] == bill_id), None)
    if bill:
        bill["status"] = "Paid"
        flash(f"Payment recorded for bill #{bill_id}.", "success")
    return redirect(url_for("billing"))

@app.route("/search")
def search():
    q = request.args.get("q", "").strip().lower()
    results = {
        "patients": [p for p in patients if q and q in " ".join(str(v) for v in p.values()).lower()],
        "doctors": [d for d in doctors if q and q in " ".join(str(v) for v in d.values()).lower()],
        "appointments": [a for a in appointments if q and q in " ".join(str(v) for v in a.values()).lower()],
        "bills": [b for b in bills if q and q in " ".join(str(v) for v in b.values()).lower()],
    }
    return render_template("search.html", q=q, results=results, active="search")

if __name__ == "__main__":
    app.run(debug=True)
