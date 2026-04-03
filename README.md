# 🏥 Hospital Management System (HMS)

A full-featured Hospital Management System built with Python and MySQL, designed for Ghanaian clinics and healthcare facilities.

---

## 📋 Features

- **Patient Management** - Register, update, view patient records with Ghana Card verification
- **Doctor Management** - Doctor profiles, specializations, availability tracking
- **Appointments** - Book appointments with conflict detection, cancel with status protection
- **Billing** - Auto-generate bills, track payments, flag overdue bills, financial summary
- **Inventory** - Medicine and equipment tracking with low stock alerts
- **Medical Records** - Clinical notes, diagnoses, lab tests, treatment records
- **Reports** - Financial, appointment, and patient reports with CSV export
- **Authentication** - Secure login with bcrypt password hashing, 13 user roles defined

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Database:** MySQL
- **Libraries:** mysql-connector-python, python-dotenv, bcrypt, colorama, rich

---

## ⚙️ Installation

### Prerequisites
- Python 3.13+
- MySQL Server
- Git

### Steps

1. Clone the repository
```bash
git clone https://github.com/Prince2457/hospital-management-system.git
cd hospital-management-system
```

2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create your `.env` file
```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=hospital_db
```

5. Set up the database
```bash
mysql -u your_mysql_username -p hospital_db < schema.sql
```

6. Run the application
```bash
python main.py
```

---

## 📁 Project Structure
```
hospital_management/
├── config/
│   └── db.py                  # Database connection
├── models/
│   ├── patient.py             # Patient class
│   ├── doctor.py              # Doctor class
│   ├── appointment.py         # Appointment class
│   ├── billing.py             # Billing class
│   ├── inventory.py           # Inventory class
│   └── medical_record.py      # Medical Record class
├── utils/
│   ├── patients.py            # Patient CRUD
│   ├── doctors.py             # Doctor CRUD
│   ├── appointments.py        # Appointment CRUD + business logic
│   ├── billing.py             # Billing CRUD + financial logic
│   ├── inventory.py           # Inventory CRUD
│   ├── medical_records.py     # Medical Records CRUD
│   ├── auth.py                # Authentication + bcrypt
│   ├── reports.py             # Reports + CSV export
│   ├── db_helpers.py          # Reusable execute_query
│   └── menu_helpers.py        # Shared UI helpers
├── tests/
│   ├── test_auth.py           # Auth unit tests
│   └── test_appointments.py   # Appointment unit tests
├── reports/                   # Generated CSV reports
├── venv/                      # Virtual environment
├── schema.sql                 # Database schema
├── requirements.txt
├── .env                       # Database credentials (gitignored)
├── .gitignore
├── README.md
└── main.py                    # Application entry point
```

---

## 🔐 Security

- Passwords hashed with bcrypt — never stored in plain text
- Parameterized queries — SQL injection protected
- Environment variables — credentials never hardcoded
- Role-based access — 13 user roles defined

---

## 👨‍💻 Built By

**Prince Nkansah** — Ghana 🇬🇭  
GitHub: [@Prince2457](https://github.com/Prince2457)  
Building toward African healthtech — one week at a time.

---

## 🗺️ Roadmap

- [x] Phase 1 — CLI Application with full CRUD, auth, reports
- [ ] Phase 1.5 — Role-based access control (permissions per role)
- [ ] Phase 2 — DSA + Algorithm optimization
- [ ] Phase 3 — FastAPI REST API + React frontend + Docker deployment
- [ ] Phase 4 — Flutter mobile app + AI features + SaaS for Ghana clinics