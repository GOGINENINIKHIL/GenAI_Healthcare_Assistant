import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, BulkWriteError

# --- Configuration ---
# IMPORTANT: Update this path to where your Synthea output is located
SYNTHEA_OUTPUT_DIR = r"E:\Tools\synthea\output\fhir" 

MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE_NAME = "healthcare_assistant_db"
COLLECTION_NAME = "patients"

# --- Main Logic ---

async def load_data():
    """
    Connects to MongoDB, finds Synthea JSON files, parses them, 
    and inserts simplified patient records into the database.
    """
    # --- Connect to MongoDB ---
    print("Attempting to connect to MongoDB...")
    try:
        client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
        await client.admin.command('ismaster') # Check connection
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print("Successfully connected to MongoDB.")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return

    # --- Find Synthea Files ---
    if not os.path.exists(SYNTHEA_OUTPUT_DIR):
        print(f"Error: Directory not found -> {SYNTHEA_OUTPUT_DIR}")
        print("Please make sure the SYNTHEA_OUTPUT_DIR path is correct.")
        client.close()
        return

    json_files = [f for f in os.listdir(SYNTHEA_OUTPUT_DIR) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files to process in {SYNTHEA_OUTPUT_DIR}")

    if not json_files:
        print("No JSON files found to process.")
        client.close()
        return
        
    # --- Process and Insert Data ---
    all_simplified_patients = []
    for file_name in json_files:
        file_path = os.path.join(SYNTHEA_OUTPUT_DIR, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # FHIR bundles contain a list of 'entry' items
            if 'entry' not in data:
                continue

            # This dictionary will hold our simplified patient record
            simplified_patient = {
                "conditions": [],
                "medications": [],
                "reports_text": [] # To store plain text from diagnostic reports
            }

            # Loop through all resources in the bundle
            for entry in data['entry']:
                resource = entry.get('resource', {})
                resource_type = resource.get('resourceType')

                # Extract Patient Info
                if resource_type == 'Patient':
                    patient_id = resource.get('id')
                    name_data = resource.get('name', [{}])[0]
                    simplified_patient['_id'] = patient_id # Use patient ID as document ID
                    simplified_patient['name'] = f"{' '.join(name_data.get('given', []))} {name_data.get('family', '')}"
                    simplified_patient['gender'] = resource.get('gender')
                    simplified_patient['birthDate'] = resource.get('birthDate')
                
                # Extract Conditions
                elif resource_type == 'Condition':
                    condition_text = resource.get('code', {}).get('text')
                    if condition_text:
                        simplified_patient['conditions'].append(condition_text)

                # Extract Medications
                elif resource_type == 'MedicationRequest':
                    med_text = resource.get('medicationCodeableConcept', {}).get('text')
                    if med_text:
                        simplified_patient['medications'].append(med_text)
                        
                # Extract Text from Diagnostic Reports
                elif resource_type == 'DiagnosticReport':
                    report_text = resource.get('text', {}).get('div')
                    if report_text:
                        # The text is often wrapped in HTML tags like <div>, so we just add the raw snippet.
                        # For a real app, you would parse the HTML to get clean text.
                        simplified_patient['reports_text'].append(report_text)
            
            if '_id' in simplified_patient: # Only add if we found a patient resource
                all_simplified_patients.append(simplified_patient)

    # --- Bulk Insert into MongoDB ---
    if all_simplified_patients:
        print(f"\nAttempting to insert {len(all_simplified_patients)} patient records...")
        try:
            # First, delete existing records to avoid duplicates on re-runs
            await collection.delete_many({})
            print("Cleared existing patient records from the collection.")
            
            # Insert new records
            result = await collection.insert_many(all_simplified_patients)
            print(f"Successfully inserted {len(result.inserted_ids)} records into '{COLLECTION_NAME}' collection.")
        except BulkWriteError as bwe:
            print(f"A bulk write error occurred: {bwe.details}")
        except Exception as e:
            print(f"An error occurred during database insertion: {e}")

    # --- Close Connection ---
    client.close()
    print("MongoDB connection closed.")


if __name__ == "__main__":
    # This allows you to run the script directly from the command line
    asyncio.run(load_data())