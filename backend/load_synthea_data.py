import os
import json
import asyncio
import base64
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# --- Configuration ---
SYNTHEA_OUTPUT_DIR = r"E:\Tools\synthea\output\fhir" 
MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE_NAME = "healthcare_assistant_db"
COLLECTION_NAME = "patients"

# --- Main Logic ---

def get_patient_id_from_reference(reference_str):
    """Helper function to extract patient ID from a reference string like 'urn:uuid:...'"""
    return reference_str.replace("urn:uuid:", "")

async def load_data():
    """
    Connects to MongoDB, finds Synthea JSON files, aggregates data, 
    assembles patient records (without conditions/meds), and inserts them.
    """
    print("--- SCRIPT START ---")
    try:
        client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
        await client.admin.command('ismaster')
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print("Successfully connected to MongoDB.")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return

    if not os.path.exists(SYNTHEA_OUTPUT_DIR):
        print(f"Error: Directory not found -> {SYNTHEA_OUTPUT_DIR}")
        client.close()
        return

    json_files = [f for f in os.listdir(SYNTHEA_OUTPUT_DIR) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files to process.")

    print("\n--- STAGE 1: Reading all files and gathering resources... ---")
    patients = {}
    reports = {} # We only need to gather patients and reports now

    for file_name in json_files:
        file_path = os.path.join(SYNTHEA_OUTPUT_DIR, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'entry' not in data: continue

            for entry in data['entry']:
                resource = entry.get('resource', {})
                resource_type = resource.get('resourceType')
                
                if resource_type == 'Patient':
                    patient_id = resource.get('id')
                    if patient_id:
                        name_data = resource.get('name', [{}])[0]
                        patients[patient_id] = {
                            "_id": patient_id,
                            "name": f"{' '.join(name_data.get('given', []))} {name_data.get('family', '')}",
                            "gender": resource.get('gender'),
                            "birthDate": resource.get('birthDate')
                        }

                elif resource_type == 'DiagnosticReport':
                    patient_ref_obj = resource.get('subject')
                    if not patient_ref_obj or 'reference' not in patient_ref_obj: continue
                    
                    patient_id = get_patient_id_from_reference(patient_ref_obj['reference'])
                    
                    presented_form = resource.get('presentedForm')
                    if presented_form and isinstance(presented_form, list) and len(presented_form) > 0:
                        encoded_data = presented_form[0].get('data')
                        if encoded_data:
                            decoded_bytes = base64.b64decode(encoded_data)
                            decoded_string = decoded_bytes.decode('utf-8')
                            reports.setdefault(patient_id, []).append(decoded_string)

    print(f"Gathered {len(patients)} unique patients and their report data.")
    
    print("\n--- STAGE 2: Assembling complete patient records... ---")
    final_patient_records = []
    for patient_id, patient_data in patients.items():
        # Only add the reports_text field now
        patient_data['reports_text'] = reports.get(patient_id, [])
        final_patient_records.append(patient_data)
    print(f"Assembled {len(final_patient_records)} final records.")

    if final_patient_records:
        print(f"\n--- STAGE 3: Clearing database and inserting {len(final_patient_records)} complete records... ---")
        try:
            delete_result = await collection.delete_many({})
            print(f"Cleared {delete_result.deleted_count} existing patient records.")
            
            result = await collection.insert_many(final_patient_records)
            print(f"Successfully inserted {len(result.inserted_ids)} new records.")
        except Exception as e:
            print(f"An error occurred during database insertion: {e}")

    client.close()
    print("\nMongoDB connection closed. Data loading complete.")


if __name__ == "__main__":
    asyncio.run(load_data())