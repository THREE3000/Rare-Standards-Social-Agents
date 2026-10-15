# Rare-Standards-Social-Agents
# 🤖 Autonomous Social Media Marketing Crew

**Author:** Arabia Brooks-Porter  
**Project Status:** Active / Production-Ready  
**Tech Stack:** Python, CrewAI, Ollama (Llama 3.1), LangChain, DuckDuckGo Search API

## 📌 Project Overview
This repository contains a locally hosted, multi-agent AI system designed to autonomously generate fact-checked, high-converting social media marketing content for **Rare Standards**, a premium Enterprise IT and Mobile Accessories e-commerce brand. 

Running entirely on local hardware (NVIDIA RTX 3060 12GB) to ensure zero API token costs and complete data privacy, this system replaces generic generative AI outputs with a strict, assembly-line production model. 

## ⚙️ The Multi-Agent Architecture
Engineered with rigorous standard operating procedures (SOPs) inspired by military logistics and cybersecurity compliance, the script utilizes a three-agent crew that cross-checks each other's work:

1. **Tech Hardware Researcher:** Equipped with a custom-built Python web-scraping tool (`duckduckgo-search`). It actively searches the internet for real-world product specifications (RPM, wattage, materials) to completely eliminate AI data hallucination.
2. **Lead Social Media Strategist:** Consumes the factual data from the Researcher and drafts highly targeted TikTok captions and Facebook posts. 
3. **Quality Assurance Editor:** Acts as the final compliance filter. It reviews the generated copy, strips out generic AI clichés, and ensures the tone aligns with a premium Enterprise IT brand.

## 🛠️ Key Features
* **Custom Tooling:** Built a robust `@tool` wrapper to bypass Pydantic dependency conflicts in standard LangChain search modules.
* **Cost-Free Local LLM:** Leverages the open-source `llama3.1` model via an Ollama server, operating entirely locally.
* **Sequential Processing:** Forces a strict `Process.sequential` pipeline so no marketing copy is generated without prior factual validation. 

## 🚀 How to Run Locally
1. Clone this repository.
2. Initialize the virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt` *(Note: requires crewai, langchain-openai, duckduckgo-search)*
5. Ensure Ollama is running locally with the Llama 3.1 model.
6. Execute the script: `python main.py`
