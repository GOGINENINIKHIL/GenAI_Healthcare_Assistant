from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure # For error handling

# Your MongoDB connection string (for a local server)
MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE_NAME = "healthcare_assistant_db" # Choose a name for your database

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase() # Global object to hold the client

async def connect_to_mongo():
    print("Attempting to connect to MongoDB...")
    db.client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    try:
        # The ismaster command is cheap and does not require auth.
        await db.client.admin.command('ismaster')
        print(f"Successfully connected to MongoDB! Will use database: {DATABASE_NAME}")
    except ConnectionFailure:
        print("MongoDB connection failed. Please ensure MongoDB is running.")
        db.client = None # Set client to None if connection fails

async def close_mongo_connection():
    if db.client:
        print("Closing MongoDB connection.")
        db.client.close()
        print("MongoDB connection closed.")

async def get_database() -> AsyncIOMotorClient:
    if db.client is None:
        # This scenario should ideally be handled by ensuring connect_to_mongo is called at startup.
        # For robustness, you could attempt a reconnect or raise an error.
        print("Database client not initialized. Call connect_to_mongo at application startup.")
        # You might want to raise an exception here or handle it differently
        return None # Or raise HTTPException(status_code=500, detail="Database not connected")
    return db.client[DATABASE_NAME]

# Example of getting a specific collection (we'll use this later)
# async def get_patients_collection():
#     database = await get_database()
#     if database:
#         return database.patients # 'patients' will be the collection name
#     return None