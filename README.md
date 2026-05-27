# AI-Enhanced Smart Tour Management Platform

## Project Overview
This project is a beginner-friendly, student-style full-stack tour management web application built with Flask, Bootstrap, and a small AI stack. It combines a traditional booking workflow with:

- User and admin authentication
- Tour package browsing and booking
- Booking history and PDF export
- Random Forest-based booking prediction
- GenAI-based itinerary generation
- AI travel chatbot
- Analytics dashboard

## Features
- Register/login/logout for users
- Admin login and package management
- Search and filter tours
- Booking confirmation and payment tracking
- ML prediction page
- AI itinerary generator
- Chatbot assistant
- Analytics dashboard
- Responsive Bootstrap UI

## Technology Stack
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Python Flask
- Database: SQLite (default for local demo) and MySQL-ready SQL file
- ML: Scikit-learn, Random Forest
- Generative AI: OpenAI-compatible API
- Charts: Chart.js

## Setup
1. Open the Codespaces terminal.
2. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Train the ML model:
   ```bash
   python ml/train_model.py
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Open the URL shown in the terminal.

## Project Structure
- `backend/app.py`
- `backend/routes/`
- `backend/models/`
- `backend/templates/`
- `backend/static/`
- `backend/ai/`
- `backend/ml/`
- `backend/database.sql`
- `documentation/`

## Notes
- The default database mode is SQLite for easy local execution in Codespaces.
- The MySQL schema is available in `backend/database.sql`.
- Set `OPENAI_API_KEY` in `backend/.env` to enable AI-powered itinerary and chatbot responses.

## Future Enhancements
- Add a real payment gateway
- Provide admin booking cancellations
- Add image upload support for packages
- Improve AI prompts and recommendation logic
