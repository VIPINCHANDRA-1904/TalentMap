# TalentMap - AI Skill Gap & Career Prediction System

TalentMap is an AI-powered Career Intelligence Platform that analyzes resumes to bridge the gap between candidate qualifications and industry requirements.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-green.svg)

## 🚀 Key Features

- **ML-Powered Role Prediction**: Uses a Naive Bayes classifier with TF-IDF vectorization to predict suitable career fields and job roles.
- **Skill Gap Detection**: Automatically extracts technical skills and identifies missing competencies for the predicted role.
- **Job Match Scoring**: ATS-inspired weighted scoring algorithm calculating selection probability.
- **Company Intelligence**: Recommends top hiring companies with detailed role descriptions and competitive tier classification.
- **Interest-Based Learning**: A novel module that performs live web searches (DuckDuckGo) to dynamically generate learning roadmaps for any user-specified field.
- **Premium UI**: Modern dark-themed interface with glassmorphism design and micro-animations.

## 🛠️ Technology Stack

- **Backend**: Python (Flask)
- **Machine Learning**: Scikit-learn (Naive Bayes, TF-IDF)
- **NLP**: NLTK, spaCy
- **Parsing**: pdfminer.six, python-docx
- **Search**: DuckDuckGo API (ddgs)
- **Database**: SQLite
- **Frontend**: Glassmorphism CSS, Vanilla JS

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/VIPINCHANDRA-1904/TalentMap.git
cd TalentMap
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Data & Model
```bash
# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
# Train the initial ML model
python train_model.py
```

### 5. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:8080` in your browser.

## ☁️ Cloud Deployment (Railway)

This repository includes a `railway.toml` and `Procfile` for instant deployment on [Railway](https://railway.app/).
1. Connect your GitHub repo to Railway.
2. Railway will automatically build the app, train the model, and deploy using the configuration.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed for AI-driven Career Intelligence.*