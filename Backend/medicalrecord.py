from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mysql.connector import Error
from typing import List
from database import get_connection  # Importing get_connection from database.py

router = APIRouter(prefix="/medical_records", tags=["Medical Records"])

# Define the request model for adding/updating medical records
class MedicalRecordCreate(BaseModel):
    patient_id: str
    record_date: str
    diagnosis: str
    treatment: str
    prescription: str
    doctor_notes: str

class MedicalRecordUpdate(BaseModel):
    diagnosis: str
    treatment: str
    prescription: str
    doctor_notes: str

class MedicalRecord(MedicalRecordCreate):
    record_id: int
    created_at: str
    updated_at: str

#1. Add a new medical record to the table
@router.post("/", response_model=MedicalRecordCreate)
def add_medical_record(record: MedicalRecordCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insert a new medical record into the database
        cursor.execute(
            """INSERT INTO medical_records (patient_id, record_date, diagnosis, 
                        treatment, prescription, doctor_notes)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (record.patient_id, record.record_date, record.diagnosis,
             record.treatment, record.prescription, record.doctor_notes),
        )
        conn.commit()
        return record

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()


#2. Update a medical record in the database
@router.put("/{record_id}", response_model=MedicalRecordUpdate)
def update_medical_record(record_id: int, record: MedicalRecordUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Update the medical record in the database
        cursor.execute(
            """UPDATE medical_records
               SET diagnosis = %s, treatment = %s, prescription = %s, doctor_notes = %s
               WHERE record_id = %s""",
            (record.diagnosis, record.treatment, record.prescription, record.doctor_notes, record_id),
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")

        return record

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

#3. Get a medical record using patient_id
@router.get("/{patient_id}", response_model=List[MedicalRecord])
def get_medical_records(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Query the database for records matching the patient_id
        cursor.execute("SELECT * FROM medical_records WHERE patient_id = %s", (patient_id,))
        records = cursor.fetchall()

        if not records:
            raise HTTPException(status_code=404, detail="No medical records found for this patient")

        # Map the result to the MedicalRecord response model
        medical_records = [
            MedicalRecord(
                record_id=record["record_id"],
                patient_id=record["patient_id"],
                record_date=record["record_date"],
                diagnosis=record["diagnosis"],
                treatment=record["treatment"],
                prescription=record["prescription"],
                doctor_notes=record["doctor_notes"],
                created_at=record["created_at"],
                updated_at=record["updated_at"]
            )
            for record in records
        ]

        return medical_records

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

#4. Delete a medical record
@router.delete("/{record_id}", status_code=204)
def delete_medical_record(record_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Delete the medical record from the database using the record_id
        cursor.execute("DELETE FROM medical_records WHERE record_id = %s", (record_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()