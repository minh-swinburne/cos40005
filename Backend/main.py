from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import doctor, patient

# FastAPI app instance
app = FastAPI()
app.include_router(doctor.router)
app.include_router(patient.router)

# CORS middleware to allow cross-origin requests
origins = [
    "http://localhost",  # Allow local testing in a different port
    "http://localhost:8000",  # Allow access from localhost
    "http://127.0.0.1",  # Allow access from localhost with 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, PUT, DELETE, GET, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)