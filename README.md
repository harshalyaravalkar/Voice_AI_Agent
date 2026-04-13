# 🎤 Voice-Controlled AI Agent

## 📌 Overview
This project is a voice-controlled AI agent that processes audio input, understands user intent, and executes tasks such as file creation, code generation, and text summarization.

The system converts speech into actionable outputs using a hybrid pipeline of APIs and local LLMs.

---

## 🚀 Features
- 🎤 Audio input (Microphone + File Upload)
- 🧠 Speech-to-Text using Groq Whisper API
- 🤖 Intent Detection using Local LLM (Ollama - phi)
- ⚙️ Tool Execution:
  - File creation
  - Code generation
  - Text summarization
- 📁 Dynamic filename extraction
- 🖥️ Interactive UI using Gradio

---

## 🧠 Architecture

Gradio UI → Groq (Whisper API via Requests) → Ollama (phi model) → Python Execution Layer → Output Interface

---

## 🛠️ Tech Stack
- Python
- Gradio
- Groq API (Speech-to-Text)
- Ollama (Local LLM - phi)
- Requests
- python-dotenv
- re (Regex for filename extraction)

---

## 📂 Project Structure
Voice_AI_Agent/
- app.py
- README.md
- .env (not included in repo)
- output/ (created at runtime)

---

## 🔐 Setting Up Groq API Key

### Step 1: Get API Key
1. Go to: https://console.groq.com/keys
2. Create a new API key
3. Copy the key

---

### Step 2: Set API Key (Windows CMD / PowerShell)

#### Permanent
```cmd
setx GROQ_API_KEY "your_api_key_here""
```
⚠️ After using `setx`, restart terminal before running the app.

---

### Step 3: (Optional) Using `.env` file

Create a `.env` file in project root:

GROQ_API_KEY=your_api_key_here

---

## ⚙️ Installation & Setup

### 1. Clone Repository
git clone https://github.com/your-username/Voice_AI_Agent.git
cd Voice_AI_Agent

---

### 2. Install Dependencies
pip install gradio requests groq python-dotenv

---

### 3. Install Ollama

Download from: https://ollama.com/

Run:
ollama run phi

(This loads the local LLM model)

---

### 4. Run Application
python app.py

---

## 📁 Output Folder

- The `output/` folder is automatically created when the app runs.
- All generated files (code, text files) are stored inside this folder.

---

## 🎯 Example Commands

- "Create a Python file for palindrome"
- "Write a function for binary search"
- "Create a file named test.txt"
- "Summarize this text..."

---

## ⚠️ Design Decisions

- Groq API used for fast and reliable speech-to-text (local Whisper was too slow)
- Ollama (phi) used for local LLM inference to satisfy assignment requirements
- Hybrid approach ensures both performance and local execution

---

## ⚠️ Challenges Faced

- Slow local Whisper model → switched to Groq API  
- Inconsistent LLM outputs → added cleaning + rules  
- Intent detection errors → hybrid LLM + rule-based system  
- Filename extraction → implemented regex-based solution  

---

## 🎥 Demo Video
[(Demo Video)](https://youtu.be/SDdVtu5xTPg)

---

## ✍️ Article
[(Building AI Agent - Medium Article)](https://medium.com/@harshal.y.492/building-a-voice-controlled-ai-agent-using-groq-and-ollama-076d0fd9a573)

---

## 🏁 Conclusion

This project demonstrates how to build a real-world AI agent that integrates speech processing, language understanding, and action execution into a unified pipeline.

It showcases the transition from passive AI systems to action-oriented intelligent agents.
