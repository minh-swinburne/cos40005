from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from typing import Optional
from pydantic import BaseModel
from mysql.connector import Error
import uuid  # Import uuid for UUID generation

# FastAPI app instance
router = APIRouter(prefix="/patients", tags=["Patients"])

# Pydantic model for patient data validation
class Patient(BaseModel):
    full_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None

# 1. Add a new patient
@router.post("/patients")
def add_patient(patient: Patient):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        patient_id = str(uuid.uuid4())  # Generate a UUID for the patient
        query = """
        INSERT INTO patients (
            patient_id, full_name, phone_number, email, address, date_of_birth, 
            gender, emergency_contact, medical_history
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            patient_id,
            patient.full_name,
            patient.phone_number,
            patient.email,
            patient.address,
            patient.date_of_birth,
            patient.gender,
            patient.emergency_contact,
            patient.medical_history,
        )
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Patient added successfully", "patient_id": patient_id}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add patient: {e}")
    finally:
        cursor.close()
        connection.close()

# 2. Update patient information
@router.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        UPDATE patients
        SET full_name = %s, phone_number = %s, email = %s, address = %s, 
            date_of_birth = %s, gender = %s, emergency_contact = %s, medical_history = %s
        WHERE patient_id = %s
        """
        values = (
            patient.full_name,
            patient.phone_number,
            patient.email,
            patient.address,
            patient.date_of_birth,
            patient.gender,
            patient.emergency_contact,
            patient.medical_history,
            patient_id
        )
        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")

        return {"message": "Patient information updated successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update patient: {e}")
    finally:
        cursor.close()
        connection.close()

# 3. Delete patient
@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "DELETE FROM patients WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")

        return {"message": "Patient deleted successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete patient: {e}")
    finally:
        cursor.close()
        connection.close()

# 4. Get all patients
@router.get("/patients")
def get_all_patients():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM patients"
        cursor.execute(query)
        patients = cursor.fetchall()

        if not patients:
            return {"message": "No patients found."}

        return {"patients": patients}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patients: {e}")
    finally:
        cursor.close()
        connection.close()

# 5. Get patient information by UUID
@router.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM patients WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        return patient
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient: {e}")
    finally:
        cursor.close()
        connection.close()
