import gradio as gr
import os
import requests
from groq import Groq
import re
from dotenv import load_dotenv

load_dotenv()

# Load model
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("API KEY:", os.getenv("GROQ_API_KEY"))

# output folder
os.makedirs("output", exist_ok=True)

def transcribe_audio(audio):
    with open(audio, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3"
        )
    return transcription.text


# Intent Detection
def detect_intent(text):
    text_lower = text.lower()

    # ✅ fallback rule for summary
    if "summarize" in text_lower or "summary" in text_lower:
        return "SUMMARIZE"
    
    # ✅ strong rule for combined intent
    if "create" in text_lower and (
    "code" in text_lower or 
    "function" in text_lower or 
    "program" in text_lower or
    "write" in text_lower
    ):
        return "CREATE_FILE + WRITE_CODE"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": f"""
Classify the intent into EXACTLY one of these labels:

CREATE_FILE
WRITE_CODE
CREATE_FILE + WRITE_CODE
SUMMARIZE
GENERAL_CHAT

Rules:
- If user asks to create file AND code → CREATE_FILE + WRITE_CODE
- If only code → WRITE_CODE
- If only file → CREATE_FILE
- If summary → SUMMARIZE
- Else → GENERAL_CHAT

Sentence: "{text}"

Return ONLY the label. No numbers. No explanation.
""",
                "stream": False
            },
            timeout=30
        )

        result = response.json()
        raw_intent = result.get("response", "").strip().upper()

        # ✅ CLEAN OUTPUT
        if "CREATE_FILE" in raw_intent and "WRITE_CODE" in raw_intent:
            return "CREATE_FILE + WRITE_CODE"
        elif "WRITE_CODE" in raw_intent:
            return "WRITE_CODE"
        elif "CREATE_FILE" in raw_intent:
            return "CREATE_FILE"
        elif "SUMMARIZE" in raw_intent:
            return "SUMMARIZE"
        else:
            return "GENERAL_CHAT"

    except:
        return "GENERAL_CHAT"

# Code Cleaner
def clean_code(code):
    code = code.replace("```python", "").replace("```", "").strip()

    # Remove everything after first double newline (junk starts here)
    if "\n\n" in code:
        code = code.split("\n\n")[0]

    return code


# Code Generator
def generate_code(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": f"Write a short simple Python function for: {prompt}. Only code. No explanation.",
                "stream": False
            },
            timeout=120
        )

        result = response.json()

        # ✅ APPLY CLEANING HERE
        return clean_code(result.get("response", "No code generated"))

    except Exception as e:
        return f"Error generating code: {str(e)}"


# Tool Execution
def summarize_text(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": f"Summarize this text in 2-3 lines:\n{text}",
                "stream": False
            },
            timeout=60
        )

        result = response.json()
        return result.get("response", "No summary generated")

    except Exception as e:
        return f"Error summarizing: {str(e)}"

def extract_filename(text):
    match = re.search(r"(?:named|called)\s+([a-zA-Z0-9_\-]+\.[a-zA-Z]+)", text.lower())
    if match:
        return match.group(1)
    return None

def execute_action(intent, text):
    try:
        # CREATE FILE + WRITE CODE
        
        if intent == "CREATE_FILE + WRITE_CODE":
            filename_extracted = extract_filename(text)

            if filename_extracted:
                filename = f"output/{filename_extracted}"
            else:
                filename = "output/generated_code.py"

            code = generate_code(text)

            with open(filename, "w") as f:
                f.write(code)

            return f"✅ File created and code written successfully: {filename}"
        
        # CREATE EMPTY FILE
        elif intent == "CREATE_FILE":
            filename_extracted = extract_filename(text)

            if filename_extracted:
                filename = f"output/{filename_extracted}"
            else:
                filename = "output/new_file.txt"

            with open(filename, "w") as f:
                f.write("")

            return f"✅ Empty file created: {filename}"

        # WRITE CODE ONLY
        elif intent == "WRITE_CODE":
            filename = "output/code_only.py"

            code = generate_code(text)

            with open(filename, "w") as f:
                f.write(code)

            return f"✅ Code written successfully: {filename}"

        # SUMMARIZATION
        elif intent == "SUMMARIZE":
            summary = summarize_text(text)
            return f"📄 Summary:\n{summary}"

        # GENERAL CHAT
        else:
            return "💬 General chat response (can be extended)"

    except Exception as e:
        return f"❌ Error during execution: {str(e)}"

# Main Pipeline
def process_audio(audio):
    try:
        if audio is None:
            return "No audio", "No intent", "No action"

        # Step 1: STT
        text = transcribe_audio(audio)

        # Step 2: Intent
        intent = detect_intent(text)

        # Step 3: Action
        action_result = execute_action(intent, text)

        return text, intent, action_result

    except Exception as e:
        return "Error", "Error", str(e)

# UI
with gr.Blocks() as app:
    gr.Markdown("# 🎤 Voice AI Agent")

    audio_input = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Upload or Record Audio"
    )

    transcribed_text = gr.Textbox(label="Transcribed Text")
    detected_intent = gr.Textbox(label="Detected Intent")
    action_output = gr.Textbox(label="Action Result")

    submit_btn = gr.Button("Process")

    submit_btn.click(
        fn=process_audio,
        inputs=audio_input,
        outputs=[transcribed_text, detected_intent, action_output]
    )

app.launch()