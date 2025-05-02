# main.py
import os
import threading
from fastapi import FastAPI
from pydicom import dcmread
from receiver import start_dicom_server

app = FastAPI()
STORE_DIR = "received_dicoms"

# Background thread for DICOM SCP
@app.on_event("startup")
def start_dicom_receiver():
    thread = threading.Thread(target=start_dicom_server, daemon=True)
    thread.start()

@app.get("/dicoms")
def list_received_dicoms():
    dicom_files = [f for f in os.listdir(STORE_DIR) if f.endswith(".dcm")]
    return {"files": dicom_files}

@app.get("/dicoms/{filename}")
def view_dicom_metadata(filename: str):
    filepath = os.path.join(STORE_DIR, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    ds = dcmread(filepath)
    return {
        "PatientName": str(ds.get("PatientName", "Unknown")),
        "Modality": ds.get("Modality", "Unknown"),
        "StudyDate": ds.get("StudyDate", "Unknown"),
        "SOPInstanceUID": ds.get("SOPInstanceUID", "Unknown"),
    }
