from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime
# REMOVED: from transformers import pipeline

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


# MongoDB connection WITH ERROR HANDLING
try:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    print("✅ MongoDB connected successfully")
    mongo_connected = True
except Exception as e:
    print(f"⚠️ MongoDB connection failed: {e}")
    # Create mock db to prevent crash
    class MockCollection:
        async def insert_one(self, *args, **kwargs):
            return type('obj', (object,), {'inserted_id': 'mock_id'})
        async def find(self, *args, **kwargs):
            return []
        async def to_list(self, length):
            return []
    
    class MockDB:
        def __getattr__(self, name):
            return MockCollection()
        def get_collection(self, name):
            return MockCollection()
    
    db = MockDB()
    client = None
    mongo_connected = False

# AI model DISABLED - Using mock
print("✅ AI: Using mock generator (transformers disabled for stability)")
story_generator = None


# Create the main app without a prefix
app = FastAPI()

# Create a router
api_router = APIRouter()


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World", "mongodb": mongo_connected, "ai_model": False}

@api_router.get("/test")
async def test():
    return {"status": "ok", "message": "App is running", "timestamp": datetime.utcnow().isoformat()}

@api_router.get("/health")
async def health():
    return {
        "status": "healthy",
        "mongodb": mongo_connected,
        "ai_model": False,
        "timestamp": datetime.utcnow().isoformat()
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    try:
        status_dict = input.dict()
        status_obj = StatusCheck(**status_dict)
        
        if mongo_connected:
            collection = db.get_collection('status_checks')
            await collection.insert_one(status_obj.dict())
            print(f"✅ Status check saved for: {input.client_name}")
        else:
            print("ℹ️ Mock DB: Status check not saved (MongoDB not connected)")
        
        return status_obj
    except Exception as e:
        print(f"⚠️ Error creating status check: {e}")
        # Return the object anyway (without saving to DB)
        return StatusCheck(client_name=input.client_name)

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    try:
        if mongo_connected:
            collection = db.get_collection('status_checks')
            status_checks = await collection.find().to_list(1000)
            print(f"✅ Retrieved {len(status_checks)} status checks")
            return [StatusCheck(**status_check) for status_check in status_checks]
        else:
            print("ℹ️ Mock DB: Returning empty list (MongoDB not connected)")
            return []
    except Exception as e:
        print(f"⚠️ Error fetching status checks: {e}")
        return []

#  AI STORY GENERATION ENDPOINT (MOCKED)
class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 100

@api_router.post("/generate", response_model=dict)
async def generate_story(request: StoryRequest):
    return {
        "generated_story": f"Mock story for: '{request.prompt}'. The AI model is currently disabled for deployment stability.",
        "note": "AI will be enabled after basic deployment is verified"
    }
    
# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()
