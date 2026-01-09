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
from transformers import pipeline

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize AI story generator (placeholder for now) 
story_generator = pipeline('text-generation', model='distilgpt2', device=-1) 

# Placeholder AI Story Generator (To be enhanced in next branch)
story_generator = pipeline('text-generation', model='gpt2', device=-1)  # device=-1 uses CPU

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


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
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

#  AI STORY GENERATION ENDPOINT 
class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 100

@api_router.post("/generate", response_model=dict)
async def generate_story(request: StoryRequest):
    """
    Core AI prototype endpoint.
    For now, returns a mock story based on prompt keywords.
    """
    # SIMPLE MOCK LOGIC 
    story_library = {
        "mountain": "Long ago, the mountains were ancient giants who slept. They whispered secrets to the wind, which carried tales to the valleys below.",
        "river": "The river's journey began as a single tear from the sky. It learned songs from every stone and creature it passed, becoming a flowing story.",
        "forest": "The wise forest remembers every footstep. Its trees are libraries, their leaves holding stories that rustle in the dark.",
        "animal": "In the old tales, animals could speak in human tongue, sharing wisdom from a time when the world was still being dreamed.",
    }
    
    # Find matching story or return default
    prompt_lower = request.prompt.lower()
    for keyword, story in story_library.items():
        if keyword in prompt_lower:
            return {"generated_story": story}
    
    # Default response if no keyword matches
    return {"generated_story": "In the beginning, the elders spoke of a time when stories grew on trees and laughter was a currency more valuable than gold."}
    
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
    client.close()
