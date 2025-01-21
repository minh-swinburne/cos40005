from fastapi import APIRouter, HTTPException
from database import get_connection
from mysql.connector import Error
from typing import Optional
from pydantic import BaseModel
import uuid

# FastAPI app instance
router = APIRouter(prefix="/available_times", tags=["Timetable"])

# Pydantic model for timetable
class Timetable(BaseModel):
    doctor_id: str
    date: str
    start_time: str
    end_time: str
    is_available: int
    note: Optional[str]

# GET request to fetch a record by timetable_id
@router.get("/{timetable_id}")
async def get_timetable(timetable_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM timetable WHERE timetable_id = %s", (timetable_id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
        if record:
            return record
        raise HTTPException(status_code=404, detail="Timetable record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST request to add a new timetable record
@router.post("/")
async def add_timetable(timetable: Timetable):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO timetable (doctor_id, date, start_time, end_time, is_available, note)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (timetable.doctor_id, timetable.date, timetable.start_time, timetable.end_time, timetable.is_available, timetable.note)
        )
        conn.commit()
        inserted_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"message": "Timetable record added successfully", "timetable_id": inserted_id}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE request to remove a timetable record
@router.delete("/{timetable_id}")
async def delete_timetable(timetable_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM timetable WHERE timetable_id = %s", (timetable_id,))
        conn.commit()
        cursor.close()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Timetable record not found")
        return {"message": "Timetable record deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT request to update a timetable record
@router.put("/{timetable_id}")
async def update_timetable(timetable_id: int, timetable: Timetable):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE timetable SET doctor_id = %s, date = %s, start_time = %s, end_time = %s, 
               is_available = %s, note = %s WHERE timetable_id = %s""",
            (timetable.doctor_id, timetable.date, timetable.start_time, timetable.end_time,
             timetable.is_available, timetable.note, timetable_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Timetable record not found")
        return {"message": "Timetable record updated successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
