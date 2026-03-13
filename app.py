import os
import sqlite3
import pickle
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

# Import Custom Utils
from utils.resume_parser import extract_text_from_resume, extract_structured_info
from utils.skill_extractor import extract_skills
from utils.recommendation import (
    map_role_to_career_field,
    recommend_companies,
    recommend_companies_detailed,
    get_required_skills,
    get_learning_resources,
    detect_skill_gap,
    calculate_match_score
)
from utils.web_search import search_skills_for_role, search_resources_for_skill

app = Flask(__name__)
app.secret_key = 'super_secret_key_only_for_dev'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)
os.makedirs('database', exist_ok=True)

DB_PATH = 'database/talentmap.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            filename TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            extracted_skills TEXT,
            predicted_role TEXT,
            predicted_field TEXT,
            match_score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT,
            required_skills TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

model_path = 'models/role_prediction_model.pkl'
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Model not found at {model_path}. Please train it using 'python train_model.py'.")
    model = None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        flash("No file part")
        return redirect(request.url)
        
    file = request.files['resume']
    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)
        
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Step 3: Resume Parsing
        text = extract_text_from_resume(file_path)
        structured_info = extract_structured_info(text)
        
        # Step 4: Skill Extraction
        found_skills = extract_skills(text)
        session['found_skills'] = found_skills
        structured_info["skills"] = found_skills
        
        # Step 5: ML Role Prediction
        if not found_skills:
            predicted_role = "Data Analyst"
        else:
            if model:
                skills_str = " ".join(found_skills)
                predicted_role = model.predict([skills_str])[0]
            else:
                predicted_role = "Data Analyst" 
        
        # Step 6: Career Field Identification
        career_field = map_role_to_career_field(predicted_role)
        
        # Step 8, 9, 10: Skill Gaps & Match Score
        required_skills = get_required_skills(predicted_role)
        missing_skills = detect_skill_gap(found_skills, required_skills)
        match_score = calculate_match_score(found_skills, required_skills)
        
        # Step 7: Company Recommendation (uses match_score for selection chance)
        companies = recommend_companies_detailed(predicted_role, match_score)
        
        # Step 12: Database Storage
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, filename) VALUES (?, ?)", (structured_info["name"], filename))
        user_id = cursor.lastrowid
        cursor.execute(
            """INSERT INTO resume_analysis 
               (user_id, extracted_skills, predicted_role, predicted_field, match_score) 
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, ",".join(found_skills), predicted_role, career_field, match_score)
        )
        conn.commit()
        conn.close()
        
        # Clean up temp file
        os.remove(file_path)
        
        result_data = {
            "candidate_info": structured_info,
            "field": career_field,
            "role": predicted_role,
            "match_score": match_score,
            "extracted_skills": found_skills if found_skills else ["None detected"],
            "missing_skills": missing_skills if missing_skills else ["None"],
            "companies": companies
        }
        
        return render_template('result.html', result=result_data)

@app.route('/other_interests', methods=['GET', 'POST'])
def other_interests():
    if request.method == 'POST':
        field = request.form.get('field', 'Technology')
        role = request.form.get('role', 'Developer')
        
        # Step 1: Search the web for accurate required skills
        print(f"[TalentMap] Searching web for: {role} in {field}...")
        required_skills = search_skills_for_role(field, role)
        
        # Step 2: For each skill, search the web for learning resources
        learning_roadmap = []
        for skill in required_skills:
            print(f"[TalentMap] Finding resources for: {skill}")
            resources = search_resources_for_skill(skill, role)
            learning_roadmap.append({
                "skill": skill,
                "resources": resources
            })
        
        result_data = {
            "field": field,
            "role": role,
            "required_skills": required_skills,
            "learning_roadmap": learning_roadmap,
            "companies": recommend_companies(role)
        }
        return render_template('interest_result.html', result=result_data)
        
    return render_template('other_interests.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
