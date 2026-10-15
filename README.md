# CarePlus — Hospital Management System

A modern, responsive Flask mini-project for managing patient records, doctors, appointments, and billing. It uses **sample data stored in Python lists**; there is no database.

## Features
- Responsive dashboard with key metrics and upcoming appointments
- Patient registration and patient search
- Doctor directory, adding doctors, and specialty information
- Appointment booking, conflict checking, and status updates
- Billing creation, payment tracking, and invoice search
- Global search across patients, doctors, appointments, and bills
- Light/dark mode toggle
- Form validation and flash messages
- Mobile-friendly navigation

## Requirements
- Python 3.9 or newer
- pip

## Run locally
1. Extract the ZIP file and open a terminal in the `hospital_management_system` folder.
2. (Recommended) Create a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the app:
   `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.

## Project structure
```text
hospital_management_system/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── patients.html
│   ├── doctors.html
│   ├── appointments.html
│   ├── billing.html
│   └── search.html
└── static/
    ├── style.css
    └── app.js
```

## Important demo-mode notes
- All records are held in memory and **reset when the Flask server restarts**.
- This project is for learning/demo use, not real hospital operations.
- It has no login or access controls. Do not enter real patient or health information.
- For production, use a persistent database, authentication, authorization, CSRF protection, audit logging, secure deployment settings, and applicable health-data privacy controls.
- Change `app.secret_key` before any deployment. Do not use Flask debug mode in production.

## Troubleshooting
- If Flask is missing, run `pip install -r requirements.txt`.
- If port 5000 is already in use, change the last line of `app.py` to `app.run(debug=True, port=5001)` and open `http://127.0.0.1:5001`.
