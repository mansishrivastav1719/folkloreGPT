# FolkloreGPT: AI-Powered Indigenous Storyteller

**🎯 Hackathon Theme:** AI/ML (Natural Language Processing, Cultural Preservation)

**📅 Round 2 Submission**

## 📖 Problem Statement

Indigenous folklore, oral histories, and native languages are disappearing rapidly. Most existing digital archives are static and fail to capture the living, narrative nature of these traditions. They lack interaction, cultural context, and accessibility for younger generations.


## 💡 Solution Overview

*FolkloreGPT* is an AI-powered storytelling platform designed to preserve, generate, and share culturally grounded folklore narratives. The system combines a robust data collection pipeline with a scalable AI architecture to ensure stories remain authentic, contextual, and engaging.

Our approach prioritizes *responsible AI* by building on structured, community-sourced data rather than unverified text generation.


## 🧭 Evolution from Round 1 to Round 2

### Round 1 Focus
- Built *FolkloreBase*, a full-stack folklore data collection system
- Enabled text, audio, and image uploads
- Designed metadata-rich storage for future AI training

### Round 2 Focus
- Integrated AI story generation
- Designed complete system architecture
- Deployed live backend services
- Planned scalability, reliability, and real-world execution


## 🧱 System Architecture

### High-Level Architecture
The platform follows a *dual-backend architecture* to separate data ingestion from AI processing.

*Components:*
- React Frontend
- Node.js Data Ingestion Service
- Python FastAPI AI Service
- MongoDB Database
- Cloudinary Media Storage
- Railway Cloud Deployment


### 🔹 Frontend (React.js)
- Story submission interface  
- Media upload forms  
- AI story generation UI  
- Communicates with backend services via REST APIs  


### 🔹 Backend 1: Node.js Data Ingestion Service
*Responsibilities:*
- Handles multipart uploads (text, audio, images)  
- Uses multer for file handling  
- Uploads media to Cloudinary CDN  
- Stores structured metadata in MongoDB  
- Implements validation and error handling to prevent data loss  

*Why separate?*  
Ensures uninterrupted folklore data collection even if AI services are updated or redeployed.


### 🔹 Backend 2: Python FastAPI AI Service
*Responsibilities:*
- Hosts AI inference endpoints  
- Loads transformer models at startup  
- Exposes /api/generate and /api/health endpoints  
- Designed for future fine-tuning and RAG integration  

FastAPI was chosen for its async performance, clarity, and suitability for ML workloads.


## 🔄 Data Flow

1. User submits folklore content via frontend  
2. Node.js server processes uploads  
3. Media stored on Cloudinary  
4. Metadata stored in MongoDB  
5. AI service retrieves curated or generated stories  
6. Generated output returned to frontend  

This pipeline ensures clean separation between *data integrity* and *AI experimentation*.

### 📊 System Diagrams
![Data Flow Diagram](docs/download.png)
*Diagram showing data flow through our system*
This diagram illustrates FolkloreGPT’s dual-backend data flow, where Node.js handles reliable data input and media storage, while FastAPI manages AI inference and story generation. This separation ensures scalability, stability, and safe AI experimentation.


## 🧠 AI Model Strategy

### Current Implementation
- *Model:* distilgpt2  
- Chosen for low memory footprint and fast inference  
- Suitable for hackathon deployment constraints  

### Future Strategy
- Fine-tune flan-t5-base on curated folklore data  
- Implement *Retrieval-Augmented Generation (RAG)* to:  
  - Ground outputs in real folklore  
  - Reduce hallucinations  
  - Preserve cultural accuracy  

Fallback logic ensures curated stories are served if AI inference fails.


## 📈 Scalability & Reliability Plan

### Handling Increased User Load
- Stateless backend services enable horizontal scaling  
- Media served via Cloudinary CDN  
- Database indexing on frequently queried fields  

### Performance Optimization
- AI models loaded once at startup  
- Async FastAPI endpoints  
- Cached folklore embeddings for RAG queries  

### Failure Recovery
- Health check endpoints for monitoring  
- Graceful degradation to curated story mode  
- Database retry mechanisms  
- Independent backend services prevent cascading failures  


## ☁️ Deployment Details
FolkloreGPT is deployed and fully functional with real AI story generation.

### **Live Backend API **
- **URL:** `https://folkloregpt-production.up.railway.app/api/`
- **Status:** ✅ **AI Model Enabled** (distilgpt2)
- **Health Check:** `GET /api/` returns `{"message": "Hello World", "mongodb": true, "ai_model": true}`


### ☁️ Configuration

- **Platform:** Railway (Free Tier)  
- **Memory:** 512MB RAM  
- **AI Mode:** Curated + DistilGPT-2  
- **Production Toggle:** `ai_model_loaded = true`  

Memory-optimized deployment ensures reliable availability during evaluation.


### 🛣️ Execution Roadmap

#### **Phase 1 – Data Foundation (Completed)**
- Developed **FolkloreBase**, a robust platform for structured folklore collection  
- Handled text, audio, and image uploads with metadata  
- Designed MongoDB schema for cultural context and story metadata  
- Stored media in Cloudinary for reliability and scalability  

#### **Phase 2 – AI Integration & Deployment (Completed)**
- Integrated transformer-based AI model (`distilgpt2`) for story generation  
- Built AI endpoints with FastAPI (`/api/generate` and `/api/health`)  
- Maintained dual-backend architecture for stability and separation of concerns  
- Deployed live backend on Railway with health checks and memory optimization  
- Implemented fallback to curated stories to ensure reliability  
- Demonstrated fully functional end-to-end workflow in a 3-minute demo  

#### **Phase 3 – Advanced Intelligence & Scale (Post-Hackathon)**
- Fine-tuning larger instruction models (e.g., `flan-t5`) on curated folklore  
- Implementing **Retrieval-Augmented Generation (RAG)** for grounded outputs  
- Adding text-to-speech for spoken-word folklore  
- Enabling multilingual story generation  
- Containerizing the system with Docker for cloud deployment and autoscaling  

> **Note:** Phases 1 and 2 are fully implemented and demonstrated, with Phase 3 representing planned post-hackathon enhancements.


### 🎥 Demo

[![FolkloreGPT Demo](https://img.youtube.com/vi/jGH_CkNQ0q4/0.jpg)](https://youtu.be/jGH_CkNQ0q4?si=EXV173vn4IOlqq-o)
*Please click the image above to watch our 3-minute demo showcasing the following features:* 
- AI story generation  
- Live API functionality  
- Story submission  
- Media uploads  


### 👥 Team Contributions

- **Mansi Shrivastav** – Backend development, database schema design, data pipeline.  
- **Pankaj Singh** – Full-stack development, system architecture, AI integration planning.  
- **Priyanka Sharma** – Frontend development, UI/UX design.  
- **MD Arif** – Project coordination, documentation, testing support.



**📅 Round 1 Submission**

### 📖 The Problem
Indigenous languages, oral histories, and folklore are at risk of being lost. Current digital archives are often static, lacking interactive and engaging ways to preserve and share these living narratives in their authentic, multimodal forms (story, voice, imagery).

### 💡 Our Vision & Solution
We are building **FolkloreGPT**, a platform that uses AI to generate and share culturally-grounded stories. We believe a responsible AI must be built on a foundation of authentic, well-structured data.

For **Round 1**, we focused on **Phase 1: Building "FolkloreBase"** – a robust, full-stack data collection and management platform. This system is designed to gather the high-quality, rich folklore data (text, audio, images) necessary to train a future AI model that is accurate, respectful, and culturally aware.

3. System Architecture & Data Flow

The core logic of our prototype is a dual-backend architecture that separates data ingestion from AI processing, ensuring scalability and clean data flow for model training.

![System Architecture Diagram](dataflow.png)
*Diagram showing user interaction with frontend, dual backend servers, and data storage systems*


## Flow Explanation:
Here's how our system works in practice:
1. **The React Frontend** is where users interact with everything. It's built with a component library we set up, and it handles forms for stories and media uploads.
2. **The Node.js Data Server (`server.js`)** is our workhorse for handling uploads. When a user submits a story with an audio recording or image, this server takes over. It uses the `multer` library to process files, uploads them to our Cloudinary cloud storage, and then saves all the important info—like the story's cultural origin, language, and narrator—into our MongoDB database. We spent time getting the error handling right here so files don't get lost.
3. **The Python FastAPI Server (`server.py`)** is set up as our main API hub. For now, it handles basic app requests, but we've deliberately built it to be the future home for our AI model. All the endpoints are structured so that adding the story generator later will be straightforward.
4. **Why two backends?** We separated them so our data collection is rock-solid and never goes down, even while we're testing or updating the AI part in the future. It just makes the whole system more stable.

## 4. Prototype Demonstration
For Round 1, we focused on solving the biggest problem first: **how do you reliably collect and store the complex folklore data an AI needs to learn?** Our prototype is a fully-working pipeline for this.

[![Watch our FolkloreGPT Demo](https://img.youtube.com/vi/iPR_BBNPLVk/0.jpg)](https://youtu.be/iPR_BBNPLVk)

## 5. Our Plan for Round 2: Building the "GPT" Part
Our big goal for the next round is to plug the AI storytelling engine into the data platform we just built. Here’s our concrete, step-by-step plan:

### Phase 1: Integrate the Core AI Model
- **Add AI Libraries:** First, we'll add the necessary `transformers` and `torch` libraries to our `backend/requirements.txt` file.
- **Create the AI Endpoint:** In our existing `server.py`, we will implement a new `POST /api/generate` endpoint to handle story generation requests.
- **Fine-tune a Starter Model:** We'll begin by fine-tuning a capable but efficient model, like **`google/flan-t5-base`**, on the collection of stories we gather through our current platform.

### Phase 2: Enhance Our Data for AI Training
- **Build a Data Cleaning Pipeline:** We'll write Python scripts to systematically extract, clean, and structure the `storyText` and cultural metadata from our MongoDB database.
- **Implement a RAG System:** To make the AI's stories more accurate and grounded, we'll set up a Retrieval-Augmented Generation (RAG) pipeline. This allows the model to reference specific stories and facts from our own folklore database before generating a response.

### Phase 3: Launch Advanced Features & Go Live
- **Add Voice to Stories:** We'll leverage the `audioFiles` structure we already have to integrate a text-to-speech service, turning the AI's written stories into spoken-word audio.
- **Prepare for Deployment:** Finally, we'll containerize our entire dual-backend system using Docker. This will allow us to deploy the complete FolkloreGPT platform reliably on a cloud service like AWS or Azure.

## 👥 Team
- **Mansi Shrivastav** - Backend development & database design
- **Pankaj Singh** - Full-stack development & system architecture
- **Priyanka Sharma** - Frontend development & UI/UX
- **MD Arif** - Project coordination & documentation
