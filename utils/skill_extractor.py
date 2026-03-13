import nltk
from nltk.corpus import stopwords
import re

# Download stopwords if not present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def extract_skills(text):
    cleaned = clean_text(text)
    words = cleaned.split()
    
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if w not in stop_words]
    
    skills_list = [
        # Programming Languages
        "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust",
        "typescript", "php", "swift", "kotlin", "r", "scala", "perl",
        # Web
        "html", "css", "react", "angular", "vue", "node", "django", "flask",
        "spring", "bootstrap", "jquery", "sass", "tailwind",
        # Data & ML
        "sql", "machine learning", "deep learning", "data analysis",
        "data science", "statistics", "excel", "power bi", "tableau",
        "pandas", "numpy", "scikit", "tensorflow", "pytorch", "keras",
        "nlp", "computer vision", "big data", "hadoop", "spark",
        # Database
        "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite",
        # DevOps & Cloud
        "docker", "kubernetes", "aws", "azure", "gcp", "linux", "git",
        "jenkins", "terraform", "ansible", "ci cd",
        # Other
        "rest api", "graphql", "agile", "scrum", "jira",
        "data structures", "algorithms", "oop", "networking",
        "figma", "adobe", "photoshop", "selenium", "automation",
        "testing", "security", "blockchain", "iot"
    ]
    
    found_skills = []
    text_joined = " " + " ".join(filtered_words) + " "
    
    for skill in skills_list:
        # Avoid partial word matches using spaces around the skill
        if " " + skill + " " in text_joined:
            found_skills.append(skill.title())
            
    return found_skills
