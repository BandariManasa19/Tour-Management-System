# Setup Guide

## 1. Install Python dependencies
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Train the ML model
```bash
python ml/train_model.py
```

## 3. Run the app
```bash
python app.py
```

## 4. Configure AI API
Open `backend/.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=your-key-here
```

## 5. MySQL option
If you want MySQL, update `DB_TYPE` in `.env` and import `database.sql` manually.
