import os
from pynetdicom import AE, evt
from pynetdicom.sop_class import (
    CTImageStorage,
    MRImageStorage,
    UltrasoundImageStorage,  # Add Ultrasound SOP class
)
from pydicom.dataset import Dataset

STORE_DIR = "received_dicoms"
os.makedirs(STORE_DIR, exist_ok=True)

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    filename = f"{ds.SOPInstanceUID}.dcm"
    filepath = os.path.join(STORE_DIR, filename)
    ds.save_as(filepath, write_like_original=False)
    print(f"[✓] Received and stored: {filename}")
    return 0x0000

def start_dicom_server(ae_title='MY_AI_RECEIVER', port=11112):
    ae = AE(ae_title=ae_title)
    # Add support for Ultrasound Image Storage
    ae.add_supported_context(CTImageStorage)
    ae.add_supported_context(MRImageStorage)
    ae.add_supported_context(UltrasoundImageStorage)  # Support Ultrasound

    handlers = [(evt.EVT_C_STORE, handle_store)]
    print(f"[✓] Starting DICOM Receiver on port {port}")
    ae.start_server(("0.0.0.0", port), evt_handlers=handlers, block=True)
