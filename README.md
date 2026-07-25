# MedSafer AI - AI-Powered Drug Interaction Warning System

Detects medicine names from a photo of the label using OCR and OpenCV,
checks for interaction risks using an AI model, stores scan history in
MongoDB, and shows it in a Streamlit UI.

Tech Stack: Python, Flask, OpenCV, MongoDB, Streamlit, Tesseract OCR, Gemini API


## Backend Setup
1. `cd backend`
2. `pip install -r requirements.txt`
3. Install Tesseract OCR (Windows): https://github.com/UB-Mannheim/tesseract/wiki
4. Copy `.env.example` to `.env` and fill in `MONGODB_URI`, `GROQ_API_KEY`
5. `python app.py` — runs on port 5000

# MedSafer AI 💊

AI-powered healthcare app that detects medicine names from label photos
and provides drug interaction warnings, using OCR and an LLM.

**Stack:** Python · Flask · OpenCV · Tesseract OCR · MongoDB · Streamlit · Groq (Llama 3.3)

## How it works
1. User uploads a photo of a medicine label via the Streamlit UI
2. Backend (Flask) runs OCR (OpenCV + Tesseract) to extract label text
3. Extracted text + patient age/conditions are sent to an LLM (Groq)
   for interaction warnings and dosage cautions
4. Result is saved to MongoDB and shown in the UI, with scan history

## Project structure

backend/
app.py # Flask API (ties everything together)
ocr_service.py # Image preprocessing + text extraction
llm_service.py # Sends text to Groq for interaction advice
db_service.py # MongoDB save/fetch
config.py # Loads .env into one place
requirements.txt
frontend/
streamlit_app.py # Upload UI + scan history

## Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Install Tesseract OCR (Windows): https://github.com/UB-Mannheim/tesseract/wiki
4. Copy `.env.example` to `.env` and fill in `MONGODB_URI` and `GROQ_API_KEY`
5. `python app.py` — runs on `http://127.0.0.1:5000`

### Frontend
1. `cd frontend`
2. `streamlit run streamlit_app.py` — opens in browser (usually port 8501)

**Note:** both backend and frontend must be running simultaneously in separate terminals.

## API

- `POST /api/scan` — form-data: `image` (file), `age` (int), `conditions` (string)
  → returns `{ id, label_text, advice }`
- `GET /api/history?limit=20` — returns recent scans

## Disclaimer
This project is for educational/demo purposes only and is **not** a substitute
for professional medical advice.