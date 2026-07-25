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