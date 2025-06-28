from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import torch
from db import connect_to_mongo, close_mongo_connection, get_database

# Import the CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# --- START: THIS IS THE NEW SECTION TO ADD ---
# This defines which origins (websites) are allowed to connect to your backend.
origins = [
    "http://localhost:5173",  # The address of your React frontend
    "http://localhost",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],         # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)
# --- END: NEW SECTION ---


# Load AI model
try:
    device = 0 if torch.cuda.is_available() else -1
    explainer_pipeline = pipeline("text2text-generation", model="t5-small", device=device)
    print(f"Successfully loaded t5-small model on device: {'cuda' if device == 0 else 'cpu'}")
except Exception as e:
    print(f"Error loading model: {e}")
    explainer_pipeline = None

# Define request body model
class MedicalNote(BaseModel):
    medical_text: str

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Event handler for application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Hello World - GenAI Healthcare Assistant Backend is Running!"}


@app.get("/patients")
async def get_all_patients():
    mongo_db = await get_database()
    if not mongo_db:
        raise HTTPException(status_code=503, detail="Database service unavailable")

    # Find all documents in the 'patients' collection
    patients_cursor = mongo_db.patients.find({})

    patients_list = []
    async for patient in patients_cursor:
        # MongoDB's _id is a special ObjectId, we need to convert it to a string
        # so it can be sent as JSON.
        patient["_id"] = str(patient["_id"])
        patients_list.append(patient)

    return patients_list


@app.post("/explain_note")
async def explain_note_endpoint(note: MedicalNote):
    if not explainer_pipeline:
        raise HTTPException(status_code=503, detail="Explainer model is not available.")
    if not note.medical_text or not note.medical_text.strip():
        raise HTTPException(status_code=400, detail="Medical text cannot be empty.")

    try:
        input_text = f"summarize: {note.medical_text}"
        explanation = explainer_pipeline(input_text, max_length=150, min_length=30, do_sample=False)
        simplified_text = explanation[0]['generated_text']
        return {"original_text": note.medical_text, "simplified_explanation": simplified_text}
    except Exception as e:
        print(f"Error during explanation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")