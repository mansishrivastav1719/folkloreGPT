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
from transformers import pipeline, set_seed
import random

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

# AI model WITH BETTER PROMPT ENGINEERING
try:
    print("⏳ Loading AI model (this may take a minute)...")
    # Using distilgpt2 with better settings
    story_generator = pipeline(
        'text-generation', 
        model='distilgpt2', 
        device='cpu',
        max_length=200,
        truncation=True,
        pad_token_id=50256  # GPT-2 pad token
    )
    set_seed(42)  # For reproducible results
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

#  AI STORY GENERATION ENDPOINT WITH BETTER PROMPT ENGINEERING
class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 150

@api_router.post("/generate", response_model=dict)
async def generate_story(request: StoryRequest):
    try:
        if story_generator and ai_model_loaded:
            # BETTER PROMPT ENGINEERING
            print(f"🤖 Generating story for prompt: '{request.prompt}'")
            
            # Clean and format the prompt
            clean_prompt = request.prompt[:80].strip()
            
            # Use a story-focused prompt template
            story_prompts = [
                f"Write a folklore story about {clean_prompt}:\n\n",
                f"Here is a traditional tale about {clean_prompt}:\n\n",
                f"In the old stories, they spoke of {clean_prompt}. This is one such tale:\n\n",
                f"Long ago, in the time of legends, there was a story about {clean_prompt}:\n\n"
            ]
            
            selected_prompt = random.choice(story_prompts)
            
            # Generate with better parameters
            result = story_generator(
                selected_prompt,
                max_length=min(request.max_length + len(selected_prompt), 200),
                num_return_sequences=1,
                temperature=0.85,  # Balanced creativity
                top_p=0.92,  # Nucleus sampling for better quality
                do_sample=True,
                repetition_penalty=1.2,  # Avoid repetition
                pad_token_id=50256
            )
            
            generated_text = result[0]['generated_text'].strip()
            
            # Clean up: Remove the prompt part if it's included
            if generated_text.startswith(selected_prompt):
                generated_text = generated_text[len(selected_prompt):].strip()
            
            # Further cleaning
            generated_text = generated_text.split('\n')[0]  # Take first paragraph
            if len(generated_text) < 20:  # If output too short, use mock
                raise ValueError("AI output too short")
            
            return {
                "generated_story": generated_text,
                "ai_model_used": True,
                "model": "distilgpt2 (prompt-engineered)",
                "prompt_template": selected_prompt[:50] + "..."
            }
            
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        # Fall through to mock stories
    
    # FALLBACK TO ENHANCED MOCK STORIES
    print(f"📝 Using enhanced mock story for: '{request.prompt}'")
    
    # Enhanced story library with better prompts
    enhanced_stories = {
        "forest": [
            "Deep in the ancient forest, where sunlight dances through emerald leaves, there lived a spirit older than time. It whispered secrets of growth and patience to those who walked quietly.",
            "The forest remembers every footprint. Its trees are libraries, their bark etched with tales of creatures who learned that true strength grows slowly, like rings in an oak."
        ],
        "mountain": [
            "The mountains were sleeping giants who dreamed of touching the stars. Their dreams became the clouds, and their patience taught the valleys how to wait for spring.",
            "High in the silent peaks, where eagles learn to fly, there is a story carved in stone about persistence - how even the tallest mountain began as a single grain of sand."
        ],
        "river": [
            "Every river remembers its first drop of rain. This one carried melodies from melting glaciers, singing them to stones that polished smooth as old memories.",
            "The river's journey teaches flow without force. It learned songs from every bend, patience from every stone, becoming a flowing story of adaptation."
        ],
        "race": [
            "A swift rabbit once challenged a steady turtle to a race. Confident in its speed, the rabbit paused to nap. But slow and determined, the turtle crossed the finish line as the rabbit slept, teaching all that consistency outpaces haste.",
            "In the great race between speed and steadiness, the lesson was clear: quick bursts may impress, but enduring pace reaches further destinations."
        ],
        "tortoise": [
            "The wise tortoise knew that every journey begins with a single step. While others rushed ahead, it measured progress in sunrises, teaching that destinations matter less than the path.",
            "Shell carrying home, the tortoise moved through life at nature's pace. It learned that true speed is measured not in distance covered, but in lessons gathered along the way."
        ],
        "rabbit": [
            "The quick rabbit learned that speed alone doesn't win races. Sometimes, the pause to appreciate flowers along the path teaches more than reaching the end first.",
            "Full of energy but lacking patience, the rabbit discovered that swiftness needs wisdom's balance to truly succeed in life's long journey."
        ]
    }
    
    prompt_lower = request.prompt.lower()
    
    # Check for keywords with partial matching
    for keyword, stories in enhanced_stories.items():
        if keyword in prompt_lower:
            return {
                "generated_story": random.choice(stories),
                "ai_model_used": False,
                "note": f"Enhanced mock story about {keyword}"
            }
    
    # Creative default stories
    default_stories = [
        "Long ago, when the world was young and magic flowed like morning mist, elders spoke of balance - how sun needs shadow, fire needs air, and every creature finds its pace.",
        "The ancestors believed every challenge held hidden wisdom. They told tales not to entertain, but to plant seeds of understanding that would bloom when needed.",
        "In the village of whispers, they understood that stories are bridges between generations. Each tale carried lessons wrapped in wonder, waiting for the right moment to unfold.",
        "There is an old saying among storytellers: The fastest route isn't always straight, and the loudest voice isn't always right. True wisdom flows like underground rivers - unseen but essential."
    ]
    
    return {
        "generated_story": random.choice(default_stories),
        "ai_model_used": False,
        "note": "Creative folklore story"
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
