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


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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

# Add these imports at the top (if not already there)
from fastapi import File, UploadFile, Form
from typing import Optional
import shutil
from bson import ObjectId

# Add these new endpoints after your existing ones

# 1. Stories endpoint (for Submit page)
@api_router.post("/stories")
async def create_story(
    title: str = Form(...),
    culture: str = Form(...),
    language: str = Form(...),
    region: str = Form(...),
    category: str = Form(...),
    ageGroup: str = Form(...),
    difficulty: str = Form(...),
    description: str = Form(...),
    storyText: Optional[str] = Form(None),
    moral: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    narrator: Optional[str] = Form(None),
    submitterName: str = Form(...),
    submitterEmail: str = Form(...),
    culturalContext: Optional[str] = Form(None),
    submissionType: str = Form(...),
    audioFiles: List[UploadFile] = File(None),
    imageFiles: List[UploadFile] = File(None)
):
    try:
        # Create story document
        story_doc = {
            "title": title,
            "culture": culture,
            "language": language,
            "region": region,
            "category": category,
            "ageGroup": ageGroup,
            "difficulty": difficulty,
            "description": description,
            "storyText": storyText,
            "moral": moral,
            "tags": tags.split(",") if tags else [],
            "narrator": narrator,
            "submitterName": submitterName,
            "submitterEmail": submitterEmail,
            "culturalContext": culturalContext,
            "submissionType": submissionType,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "listeners": 0,
            "rating": 0
        }
        
        # Save audio files
        audio_paths = []
        for audio in audioFiles or []:
            if audio.filename:
                file_path = f"uploads/audio/{datetime.utcnow().timestamp()}_{audio.filename}"
                os.makedirs("uploads/audio", exist_ok=True)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(audio.file, buffer)
                audio_paths.append(file_path)
        
        # Save image files
        image_paths = []
        for image in imageFiles or []:
            if image.filename:
                file_path = f"uploads/images/{datetime.utcnow().timestamp()}_{image.filename}"
                os.makedirs("uploads/images", exist_ok=True)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                image_paths.append(file_path)
        
        story_doc["audioFiles"] = audio_paths
        story_doc["imageFiles"] = image_paths
        
        # Insert into database
        result = await db.stories.insert_one(story_doc)
        
        return {
            "success": True,
            "message": "Story submitted successfully",
            "story_id": str(result.inserted_id)
        }
        
    except Exception as e:
        logger.error(f"Story submission failed: {e}")
        return {
            "success": False,
            "message": str(e)
        }

# 2. Get all stories
@api_router.get("/stories")
async def get_stories(limit: int = 50, skip: int = 0):
    stories = await db.stories.find().skip(skip).limit(limit).to_list(limit)
    # Convert ObjectId to string
    for story in stories:
        story["_id"] = str(story["_id"])
    return stories

# 3. Get single story
@api_router.get("/stories/{story_id}")
async def get_story(story_id: str):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    if story:
        story["_id"] = str(story["_id"])
        return story
    return {"error": "Story not found"}

# 4. Contact endpoint
@api_router.post("/contact")
async def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    contact_doc = {
        "name": name,
        "email": email,
        "message": message,
        "created_at": datetime.utcnow()
    }
    result = await db.contacts.insert_one(contact_doc)
    return {
        "success": True,
        "message": "Message sent successfully",
        "contact_id": str(result.inserted_id)
    }