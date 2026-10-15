# Rare-Standards-Social-Agents
# 🤖 Autonomous Enterprise Marketing & E-Commerce Command Center

**Author:** Arabia Brooks-Porter  
**Project Status:** Active / Production-Ready  
**Architecture:** Python, CrewAI, Ollama (Llama 3.1), LangChain, DuckDuckGo Search API, MoviePy, gTTS, Make.com Webhooks, Shopify REST API  

---

## 📌 Executive Summary
This repository contains a locally hosted, multi-agent AI ecosystem engineered to autonomously manage social media marketing and e-commerce operations for **Rare Standards**, a premium consumer technology brand. 

Built to function as a fully automated corporate department, this system replaces generic, unverified generative AI outputs with a strict, assembly-line production model. By running entirely on local hardware (NVIDIA RTX 3060), the architecture ensures zero API token costs, eliminates third-party data leakage, and maintains strict operational security over proprietary business logic. 

## ⚙️ System Architecture & Departmental Modules
The ecosystem is divided into three specialized operational modules, functioning via sequential `CrewAI` agent orchestration to guarantee that all output passes through a rigorous Quality Assurance (QA) and compliance layer before deployment.

### 📱 Module 1: The Facebook Automation Engine (`main.py`)
A cross-checking text and visual curation crew that autonomously publishes verified product showcases.
* **Tech Hardware Researcher:** Actively scrapes the web via the DuckDuckGo API for real-world product specifications (RPM, wattage, materials), establishing a factual baseline to prevent LLM hallucination.
* **Lead Social Media Strategist:** Consumes the validated data and drafts highly targeted, technical marketing copy.
* **QA & Compliance Editor:** Acts as the final filter, stripping out generic AI clichés and enforcing brand voice guidelines.
* **Visual Asset Manager:** Scans the active product catalog and selects the highest-converting official Shopify media URL to pair with the approved copy.

### 🎬 Module 2: The TikTok Production Studio (`tiktok_video.py`)
An autonomous video production pipeline that renders 30fps `.mp4` commercial assets without human intervention.
* **Global CMO:** Defines the core psychological sales trigger and demographic target based on the daily product selection.
* **Executive Creative Director:** Translates the strategic brief into a high-retention, 15-second cinematic video script blueprint.
* **Brand Compliance Officer:** Sanitizes the creative output, ensuring flawless formatting for automated Text-to-Speech (TTS) rendering.
* **The Render Pipeline:** Synthesizes the voiceover using `gTTS`, downloads live high-resolution Shopify assets, stitches the audio and visuals together using `moviepy`, and routes the final encoded video file to a Make.com HTTP webhook for automated TikTok deployment.

### 💼 Module 3: Enterprise Command Center (`enterprise_command.py` & `conversion_agent.py`)
An executive intelligence crew that audits live store health and generates direct-response revenue strategies.
* **Chief Operations Officer (COO):** Queries the live Shopify store endpoint to monitor inventory telemetry, flag supply chain bottlenecks, and assess operational risk.
* **Senior UX Architect:** Identifies exact UX friction points and delivers board-room-grade structural blueprints to maximize visitor-to-buyer conversion.
* **Director of Growth:** Generates automated Abandoned Cart email sequences, rewrites product descriptions for maximum Average Order Value (AOV), and compiles findings into a comprehensive `master_executive_report.txt`.

---

## 🔐 Security & Operational Compliance
Designed with a security-first mindset, this project integrates strict operational logistics and compliance standards to safeguard business continuity:
* **Data Privacy (Zero-Leakage):** All natural language processing is handled locally via Ollama. No proprietary product strategies or customer data are transmitted to external LLM providers (e.g., OpenAI, Anthropic).
* **Anti-Duplicate Memory Logging:** Implements a state-tracking protocol (`post_history.txt`) that logs daily deployments. The system reads historical data prior to execution to cryptographically guarantee zero back-to-back duplicate posts.
* **Fail-Safe Fallbacks:** The Shopify API synchronization includes automated network-failure fallbacks, ensuring the marketing engine continues to deploy from a local redundancy catalog if the primary server goes offline.

## 🛠️ Key Technical Innovations
* **Live Shopify Catalog Sync:** Bypasses hardcoded lists by querying the live `products.json` API endpoint. New store inventory is automatically dynamically added to the AI's deployment rotation.
* **Custom Tool Wrappers:** Built robust `@tool` decorators to bypass Pydantic dependency conflicts in standard LangChain search modules.
* **Headless Automation:** Integrated entirely with Windows Task Scheduler via custom `.bat` scripts, enabling zero-touch background execution during prime e-commerce retail windows (9:30 AM, 3:00 PM, 8:00 PM).

---

## 🚀 Deployment & Installation Setup

### Prerequisites
* Python 3.10+
* Ollama installed locally with the `llama3.1` model pulled (`ollama run llama3.1`).
* Windows Task Scheduler (for headless automation).

### Installation
1. **Clone this repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/Rare-Standards-Social-Agents.git](https://github.com/YOUR-USERNAME/Rare-Standards-Social-Agents.git)
   cd Rare-Standards-Social-Agents
Initialize the virtual environment:

Bash
python -m venv venv
.\venv\Scripts\activate
Install core dependencies:

Bash
pip install crewai langchain-openai duckduckgo-search moviepy==1.0.3 gTTS requests
Execute the desired module:

Run Facebook Engine: python main.py

Run TikTok Studio: python tiktok_video.py

Run Store Audit: python enterprise_command.py

Developed to demonstrate advanced Python automation, local LLM orchestration, and enterprise-grade e-commerce operations.

https://rarestandards.tech/
