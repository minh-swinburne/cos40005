from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from mysql.connector import Error
from typing import Optional
from pydantic import BaseModel
import uuid

# FastAPI app instance
router = APIRouter(prefix="/doctors", tags=["Doctors"])

# Pydantic model for doctor data validation
class Doctor(BaseModel):
    full_name: str
    specialization: str
    phone_number: str
    email: str
    date_of_birth: str
    gender: str
    years_of_experience: int
    clinic_address: str
    description: Optional[str] = None

# 1. Add a new doctor
@router.post("/")
def add_doctor(doctor: Doctor):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        doctor_id = str(uuid.uuid4())  # Generate UUIDv4 for doctor_id
        query = """
        INSERT INTO doctors (
            doctor_id, full_name, specialization, phone_number, email, 
            date_of_birth, gender, years_of_experience, clinic_address, description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            doctor_id,
            doctor.full_name,
            doctor.specialization,
            doctor.phone_number,
            doctor.email,
            doctor.date_of_birth,
            doctor.gender,
            doctor.years_of_experience,
            doctor.clinic_address,
            doctor.description,
        )
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Doctor added successfully", "doctor_id": doctor_id}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add doctor: {e}")
    finally:
        cursor.close()
        connection.close()

# 2. Update doctor information
@router.put("/{doctor_id}")
def update_doctor(doctor_id: str, doctor: Doctor):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        UPDATE doctors
        SET full_name = %s, specialization = %s, phone_number = %s, email = %s, 
            date_of_birth = %s, gender = %s, years_of_experience = %s, clinic_address = %s, description = %s
        WHERE doctor_id = %s
        """
        values = (
            doctor.full_name,
            doctor.specialization,
            doctor.phone_number,
            doctor.email,
            doctor.date_of_birth,
            doctor.gender,
            doctor.years_of_experience,
            doctor.clinic_address,
            doctor.description,
            doctor_id
        )
        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return {"message": "Doctor information updated successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update doctor: {e}")
    finally:
        cursor.close()
        connection.close()

# 3. Delete doctor
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "DELETE FROM doctors WHERE doctor_id = %s"
        cursor.execute(query, (doctor_id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return {"message": "Doctor deleted successfully"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete doctor: {e}")
    finally:
        cursor.close()
        connection.close()

# 4. Get all doctors
@router.get("")
def get_all_doctors():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM doctors"
        cursor.execute(query)
        doctors = cursor.fetchall()

        if not doctors:
            return {"message": "No doctors found."}

        return {"doctors": doctors}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctors: {e}")
    finally:
        cursor.close()
        connection.close()
# 5. Get doctor information by UUID
@router.get("/{doctor_id}")
def get_doctor_by_id(doctor_id: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM doctors WHERE doctor_id = %s"
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()

        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return doctor
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctor: {e}")
    finally:
        cursor.close()
        connection.close()



