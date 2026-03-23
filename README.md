# 🏥 FastAPI Medical Appointment System
## 📌 Project Overview
This project is a complete backend application developed using **FastAPI** as part of internship training.
The system allows users to:
* View doctors
* Book medical appointments
* Manage doctor availability
* Perform advanced operations like search, sorting, and pagination
## 🎯 Project Objective
To build a real-world backend system implementing:
* REST APIs
* Data validation using Pydantic
* CRUD operations
* Multi-step workflows
* Advanced API features
## 🚀 Features Implemented
### ✅ Day 1 – GET APIs
* Home Route
* Get all doctors
* Get doctor by ID
* Appointments list
* Doctors summary
### ✅ Day 2–3 – POST + Validation
* Appointment booking API
* Pydantic validation
* Helper functions
### ✅ Day 4 – CRUD Operations
* Add doctor
* Update doctor availability
* Delete doctor
### ✅ Day 5 – Workflow APIs
* Book appointment
* Check-in
* Complete appointment
### ✅ Day 6 – Advanced APIs
* Search doctors
* Sort doctors
* Pagination
* Appointment search
* Combined browse API
## 🛠️ Technologies Used
* Python
* FastAPI
* Pydantic
* Uvicorn
## 📂 Project Structure
fastapi-medical-appointment/
│── main.py
│── requirements.txt
│── README.md
│── screenshots/
## ▶️ How to Run the Project
### 1️⃣ Install Dependencies
pip install fastapi uvicorn
### 2️⃣ Run the Server
uvicorn main:app --reload
### 3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs
## 📸 API Testing (Swagger)
All APIs are tested using Swagger UI.
Screenshots include:
* Q1 Home Route
* Q2 Get Doctors
* Q3 Get Doctor by ID
* ...
* Q20 Browse API
📁 All screenshots are available in the **screenshots/** folder.
## 📌 API Endpoints Summary
### 🔹 GET APIs
* `/`
* `/doctors`
* `/doctors/{doctor_id}`
* `/appointments`
* `/doctors/summary`
### 🔹 POST APIs
* `/appointments`
* `/doctors`
### 🔹 PUT API
* `/doctors/{doctor_id}`
### 🔹 DELETE API
* `/doctors/{doctor_id}`
### 🔹 Workflow APIs
* `/checkin/{appointment_id}`
* `/complete/{appointment_id}`
### 🔹 Advanced APIs
* `/doctors/search`
* `/doctors/sort`
* `/doctors/page`
* `/appointments/search`
* `/doctors/browse`
## 🎯 Key Learnings
* Building REST APIs with FastAPI
* Data validation using Pydantic
* API design and structure
* Implementing real-world workflows
* Handling query parameters (search, filter, pagination)
## 🙌 Acknowledgement
This project was completed as part of internship training.
Special thanks to **Innomatics Research Labs** for providing this learning opportunity.
## 📌 Conclusion
This project demonstrates a complete backend system using FastAPI with real-world features and best practices.
