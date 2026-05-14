# 🎤 Voice-Controlled AI Agent

A simple voice-controlled AI assistant built with Python, Gradio, Groq Whisper API, and Ollama.

The agent takes voice input from the microphone or uploaded audio files, converts speech to text, detects user intent, and performs actions like generating code, creating files, and summarizing text.

---

## Features

- Voice input through microphone or audio upload
- Speech-to-text using Groq Whisper API
- Intent detection using local Ollama model (`phi`)
- File creation support
- Code generation
- Text summarization
- Automatic filename extraction
- Gradio-based web interface

---

## Architecture

```text
Gradio UI
   ↓
Groq Whisper API (Speech-to-Text)
   ↓
Ollama (phi model for intent detection)
   ↓
Python Execution Layer
   ↓
Generated Output / Files
```
---

## Tech Stack
- Python
- Gradio
- Groq API (Speech-to-Text)
- Ollama (Local LLM - phi)
- Requests
- python-dotenv
- re (Regex)

---

## Project Structure
Voice_AI_Agent/
- app.py
- README.md
- .env (not included in repo)
- output/ (created at runtime)

---

## Setting Up Groq API Key

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
 After using `setx`, restart terminal before running the app.

---

### Step 3: (Optional) Using `.env` file

Create a `.env` file in project root:

GROQ_API_KEY=your_api_key_here

---

## Installation & Setup

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

## Output Folder

- The `output/` folder is created automatically when the application runs.
  Generated files such as text files or code files are stored there.
---

## Example Voice Commands

- "Create a Python file for palindrome"
- "Write a function for binary search"
- "Create a file named test.txt"
- "Summarize this text..."

---

## Design Decisions

- Groq Whisper API was used because local Whisper inference was too slow for real-time usage.
- Ollama with the phi model was used for local LLM-based intent detection.
- A hybrid approach was used to balance speed and local execution.

---

## Challenges Faced

- Local Whisper model performance was slow
- LLM responses were sometimes inconsistent
- Intent detection required both rule-based logic and LLM support
- Filename extraction needed regex-based cleanup

---

##  Demo Video
[(Demo Video)](https://youtu.be/SDdVtu5xTPg)

---

## Medium Article
[(Building AI Agent - Medium Article)](https://medium.com/@harshal.y.492/building-a-voice-controlled-ai-agent-using-groq-and-ollama-076d0fd9a573)

---

## Conclusion

This project combines speech recognition, language understanding, and task execution into a single workflow.

The goal was to build a practical AI agent capable of taking voice commands and performing useful actions in real time.
