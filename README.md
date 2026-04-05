# FolkloreGPT: AI-Powered Indigenous Storyteller

**🎯 Theme:** AI/ML (Natural Language Processing, Cultural Preservation)

### 📖 The Problem
Indigenous languages, oral histories, and folklore are at risk of being lost. Current digital archives are often static, lacking interactive and engaging ways to preserve and share these living narratives in their authentic, multimodal forms (story, voice, imagery).

### 💡 Our Vision & Solution
We are building **FolkloreGPT**, a platform that uses AI to generate and share culturally-grounded stories. We believe a responsible AI must be built on a foundation of authentic, well-structured data.

### 3. System Architecture & Data Flow
The core logic of our prototype is a dual-backend architecture that separates data ingestion from AI processing, ensuring scalability and clean data flow for model training.

**Flow Explanation:**
Here's how our system works in practice:
1.  **The React Frontend** is where users interact with everything. It's built with a component library we set up, and it handles forms for stories and media uploads.
2.  **The Node.js Data Server (`server.js`)** is our workhorse for handling uploads. When a user submits a story with an audio recording or image, this server takes over. It uses the `multer` library to process files, uploads them to our Cloudinary cloud storage, and then saves all the important info—like the story's cultural origin, language, and narrator—into our MongoDB database. We spent time getting the error handling right here so files don't get lost.
3.  **The Python FastAPI Server (`server.py`)** is set up as our main API hub. For now, it handles basic app requests, but we've deliberately built it to be the future home for our AI model. All the endpoints are structured so that adding the story generator later will be straightforward.
4.  **Why two backends?** We separated them so our data collection is rock-solid and never goes down, even while we're testing or updating the AI part in the future. It just makes the whole system more stable.

### 4. Prototype Demonstration
For Round 1, we focused on solving the biggest problem first: **how do you reliably collect and store the complex folklore data an AI needs to learn?** Our prototype is a fully-working pipeline for this.
[![Watch our FolkloreGPT Demo](https://youtu.be/)]
