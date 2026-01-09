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
from transformers import pipeline  # RE-ENABLED

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

# AI model WITH MEMORY OPTIMIZATION
try:
    print("⏳ Loading AI model (this may take a minute)...")
    # Using distilgpt2 - smaller than regular GPT-2
    story_generator = pipeline(
        'text-generation', 
        model='distilgpt2', 
        device='cpu',  # Force CPU usage
        max_length=100,  # Limit output length
        truncation=True  # Prevent memory issues
    )
    print("✅ AI model loaded successfully!")
    ai_model_loaded = True
except Exception as e:
    print(f"⚠️ AI model failed to load: {e}")
    print("⚠️ Falling back to mock AI generator")
    story_generator = None
    ai_model_loaded = False


# Create the main app without a prefix
app = FastAPI()

# Create a router WITH /api PREFIX - FIXED LINE
api_router = APIRouter(prefix="/api")  # 🔧 FIXED: Added prefix="/api"


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
    return {"message": "Hello World", "mongodb": mongo_connected, "ai_model": ai_model_loaded}

@api_router.get("/test")
async def test():
    return {"status": "ok", "message": "App is running", "timestamp": datetime.utcnow().isoformat()}

@api_router.get("/health")
async def health():
    return {
        "status": "healthy",
        "mongodb": mongo_connected,
        "ai_model": ai_model_loaded,
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

#  AI STORY GENERATION ENDPOINT (NOW WITH REAL AI!)
class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 100

@api_router.post("/generate", response_model=dict)
async def generate_story(request: StoryRequest):
    try:
        if story_generator and ai_model_loaded:
            # Generate story with AI
            print(f"🤖 Generating story for prompt: '{request.prompt}'")
            
            # Limit prompt length to prevent memory issues
            prompt = request.prompt[:100]  # First 100 chars only
            
            result = story_generator(
                prompt,
                max_length=min(request.max_length, 150),  # Max 150 tokens
                num_return_sequences=1,
                temperature=0.8,  # Creative but not random
                do_sample=True
            )
            
            generated_text = result[0]['generated_text'].strip()
            
            # Clean up the output
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return {
                "generated_story": generated_text,
                "ai_model_used": True,
                "model": "distilgpt2"
            }
        else:
            # Fallback to mock story
            print(f"📝 Using mock story for prompt: '{request.prompt}'")
            story_library = {
                "mountain": "Long ago, the mountains were ancient giants who slept. They whispered secrets to the wind, which carried tales to the valleys below.",
                "river": "The river's journey began as a single tear from the sky. It learned songs from every stone and creature it passed, becoming a flowing story.",
                "forest": "The wise forest remembers every footstep. Its trees are libraries, their leaves holding stories that rustle in the dark.",
                "animal": "In the old tales, animals could speak in human tongue, sharing wisdom from a time when the world was still being dreamed.",
            }
            
            prompt_lower = request.prompt.lower()
            for keyword, story in story_library.items():
                if keyword in prompt_lower:
                    return {
                        "generated_story": story,
                        "ai_model_used": False,
                        "note": "Using mock story (AI model not loaded)"
                    }
            
            return {
                "generated_story": "In the beginning, the elders spoke of a time when stories grew on trees and laughter was a currency more valuable than gold.",
                "ai_model_loaded": False,
                "note": "Using default mock story (AI model not loaded)"
            }
            
    except Exception as e:
        print(f"⚠️ Error generating story: {e}")
        return {
            "generated_story": f"Error generating story: {str(e)[:100]}",
            "ai_model_used": False,
            "error": True
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
