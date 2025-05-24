from fastapi import FastAPI, HTTPException # Added HTTPException
from pydantic import BaseModel
from transformers import pipeline
import torch

# Import database connection functions
from db import connect_to_mongo, close_mongo_connection, get_database # Import new functions

# Initialize FastAPI app
app = FastAPI()

# Load AI model (same as before)
try:
    device = 0 if torch.cuda.is_available() else -1
    explainer_pipeline = pipeline("text2text-generation", model="t5-small", device=device)
    print(f"Successfully loaded t5-small model on device: {'cuda' if device == 0 else 'cpu'}")
except Exception as e:
    print(f"Error loading model: {e}")
    explainer_pipeline = None

# Define request body model (same as before)
class MedicalNote(BaseModel):
    medical_text: str

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    # You could add other startup tasks here, like loading other resources

# Event handler for application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    # Add other cleanup tasks here if needed

@app.get("/")
async def root():
    # Example of how you might access the database if needed in an endpoint
    # (though this root endpoint doesn't need it)
    # mongo_db = await get_database()
    # if not mongo_db:
    #     raise HTTPException(status_code=503, detail="Database service unavailable")
    return {"message": "Hello World - GenAI Healthcare Assistant Backend is Running!"}

@app.post("/explain_note")
async def explain_note_endpoint(note: MedicalNote):
    if not explainer_pipeline:
        raise HTTPException(status_code=503, detail="Explainer model is not available.") # Use HTTPException
    if not note.medical_text or not note.medical_text.strip():
        raise HTTPException(status_code=400, detail="Medical text cannot be empty.") # Use HTTPException

    try:
        input_text = f"summarize: {note.medical_text}"
        explanation = explainer_pipeline(input_text, max_length=150, min_length=30, do_sample=False)
        simplified_text = explanation[0]['generated_text']
        return {"original_text": note.medical_text, "simplified_explanation": simplified_text}
    except Exception as e:
        print(f"Error during explanation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}") # Use HTTPException


# Example of an endpoint that might use the database (for future use)
# @app.post("/test_db_insert")
# async def test_db_insert(data: dict):
#     mongo_db = await get_database()
#     if not mongo_db:
#         raise HTTPException(status_code=503, detail="Database service unavailable")
#     try:
#         result = await mongo_db.test_collection.insert_one(data)
#         return {"message": "Data inserted", "inserted_id": str(result.inserted_id)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")