from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# -----------------------------
# DATA
# -----------------------------
doctors = [
    {"id": 1, "name": "Dr. Sharma", "specialization": "Cardiology", "is_available": True},
    {"id": 2, "name": "Dr. Khan", "specialization": "Dermatology", "is_available": True},
    {"id": 3, "name": "Dr. Mehta", "specialization": "Neurology", "is_available": False},
    {"id": 4, "name": "Dr. Patel", "specialization": "Orthopedic", "is_available": True},
    {"id": 5, "name": "Dr. Singh", "specialization": "Pediatric", "is_available": True},
    {"id": 6, "name": "Dr. Rao", "specialization": "General", "is_available": False},
]

appointments = []
appointment_counter = 1

# -----------------------------
# DAY 1 - GET APIs
# -----------------------------

@app.get("/")
def home():
    return {"message": "Welcome to Medical Appointment System"}

@app.get("/doctors")
def get_doctors():
    return {"total": len(doctors), "data": doctors}

# ⚠️ fixed route BEFORE {id}
@app.get("/doctors/summary")
def doctor_summary():
    available = [d for d in doctors if d["is_available"]]
    return {
        "total": len(doctors),
        "available": len(available),
        "unavailable": len(doctors) - len(available)
    }

@app.get("/appointments")
def get_appointments():
    return {"total": len(appointments), "data": appointments}

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if not doctor:
        return {"error": "Doctor not found"}
    return doctor

# -----------------------------
# DAY 2 - PYDANTIC
# -----------------------------
class AppointmentRequest(BaseModel):
    patient_name: str = Field(min_length=2)
    doctor_id: int = Field(gt=0)
    problem: str = Field(min_length=5)
    priority: str = "normal"

class NewDoctor(BaseModel):
    name: str = Field(min_length=2)
    specialization: str = Field(min_length=2)

# -----------------------------
# DAY 3 - HELPERS
# -----------------------------
def find_doctor(doctor_id):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    return None

def filter_doctors_logic(specialization=None, is_available=None):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result

# -----------------------------
# DAY 3 - FILTER API
# -----------------------------
@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    is_available: Optional[bool] = None
):
    result = filter_doctors_logic(specialization, is_available)
    return {"total": len(result), "data": result}

# -----------------------------
# DAY 2+3 - POST APPOINTMENT
# -----------------------------
@app.post("/appointments")
def book_appointment(data: AppointmentRequest):
    global appointment_counter

    doctor = find_doctor(data.doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    if not doctor["is_available"]:
        return {"error": "Doctor not available"}

    appointment = {
        "id": appointment_counter,
        "patient_name": data.patient_name,
        "doctor_name": doctor["name"],
        "problem": data.problem,
        "priority": data.priority,
        "status": "booked"
    }

    appointments.append(appointment)
    appointment_counter += 1

    return appointment

# -----------------------------
# DAY 4 - CRUD
# -----------------------------
@app.post("/doctors")
def add_doctor(doc: NewDoctor, response: Response):
    # duplicate check
    for d in doctors:
        if d["name"].lower() == doc.name.lower():
            return {"error": "Doctor already exists"}

    new_doc = {
        "id": len(doctors) + 1,
        "name": doc.name,
        "specialization": doc.specialization,
        "is_available": True
    }

    doctors.append(new_doc)
    response.status_code = 201
    return new_doc

@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    is_available: Optional[bool] = None
):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    if is_available is not None:
        doctor["is_available"] = is_available

    return doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    doctors.remove(doctor)
    return {"message": f"{doctor['name']} deleted successfully"}

# -----------------------------
# DAY 5 - WORKFLOW
# -----------------------------
@app.post("/checkin/{appointment_id}")
def checkin(appointment_id: int):
    for a in appointments:
        if a["id"] == appointment_id:
            a["status"] = "checked_in"
            return a
    return {"error": "Appointment not found"}

@app.post("/complete/{appointment_id}")
def complete(appointment_id: int):
    for a in appointments:
        if a["id"] == appointment_id:
            a["status"] = "completed"
            return a
    return {"error": "Appointment not found"}

# -----------------------------
# DAY 6 - SEARCH
# -----------------------------
@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [
        d for d in doctors
        if keyword.lower() in d["name"].lower()
        or keyword.lower() in d["specialization"].lower()
    ]

    if not result:
        return {"message": "No doctors found"}

    return {"total_found": len(result), "data": result}

# -----------------------------
# SORT
# -----------------------------
@app.get("/doctors/sort")
def sort_doctors(
    sort_by: str = "name",
    order: str = "asc"
):
    if sort_by not in ["name", "specialization"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_data = sorted(
        doctors,
        key=lambda x: x[sort_by],
        reverse=(order == "desc")
    )

    return {"sorted_by": sort_by, "order": order, "data": sorted_data}

# -----------------------------
# PAGINATION
# -----------------------------
@app.get("/doctors/page")
def paginate_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=10)
):
    start = (page - 1) * limit
    total = len(doctors)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "data": doctors[start:start + limit]
    }

# -----------------------------
# APPOINTMENT SEARCH
# -----------------------------
@app.get("/appointments/search")
def search_appointments(name: str):
    result = [
        a for a in appointments
        if name.lower() in a["patient_name"].lower()
    ]
    return {"total": len(result), "data": result}

# -----------------------------
# COMBINED BROWSE
# -----------------------------
@app.get("/doctors/browse")
def browse_doctors(
    keyword: Optional[str] = None,
    sort_by: str = "name",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    result = doctors

    # filter
    if keyword:
        result = [
            d for d in result
            if keyword.lower() in d["name"].lower()
            or keyword.lower() in d["specialization"].lower()
        ]

    # sort
    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    # pagination
    start = (page - 1) * limit
    total = len(result)

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": result[start:start + limit]
    }
