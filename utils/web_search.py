"""
Web Search Utility for TalentMap
Uses DuckDuckGo to search the internet for accurate skill roadmaps
and learning resources for any job role/field combination.
"""
import re
from ddgs import DDGS


def search_skills_for_role(field, role):
    """
    Search the web to find the required skills for a specific role in a field.
    Queries multiple search terms, aggregates results, and extracts skill keywords.
    Returns a list of skill strings (step-by-step roadmap items).
    """
    queries = [
        f"skills required to become a {role} in {field} roadmap",
        f"how to become a {role} step by step skills needed",
        f"{role} {field} essential skills beginners must learn"
    ]

    all_text = ""
    ddgs = DDGS()

    for query in queries:
        try:
            results = ddgs.text(query, max_results=4)
            for r in results:
                all_text += " " + r.get('body', '') + " " + r.get('title', '')
        except Exception:
            continue

    if not all_text.strip():
        return _fallback_skills(field, role)

    # Extract skills from aggregated web text
    skills = _extract_skills_from_text(all_text, role, field)

    if len(skills) < 3:
        return _fallback_skills(field, role)

    return skills


def search_resources_for_skill(skill, role):
    """
    Search the web for learning resources (courses, YouTube videos, websites)
    for a specific skill in the context of a role.
    Returns list of tuples: (resource_name, url)
    """
    clean_skill = re.sub(r'^\d+\.\s*', '', skill).strip()

    queries = [
        f"best free course to learn {clean_skill} for {role} beginners",
        f"{clean_skill} tutorial YouTube free course"
    ]

    resources = []
    ddgs = DDGS()

    for query in queries:
        try:
            results = ddgs.text(query, max_results=3)
            for r in results:
                title = r.get('title', 'Learning Resource')
                url = r.get('href', '')
                if url and url.startswith('http'):
                    # Clean up title
                    title = title[:80] if len(title) > 80 else title
                    resources.append((title, url))
        except Exception:
            continue

    # Deduplicate by URL
    seen_urls = set()
    unique = []
    for name, url in resources:
        if url not in seen_urls:
            seen_urls.add(url)
            unique.append((name, url))
        if len(unique) >= 4:
            break

    if not unique:
        # Fallback: generate dynamic search links
        search_term = clean_skill.replace(' ', '+')
        unique = [
            (f"YouTube: Learn {clean_skill}", f"https://www.youtube.com/results?search_query={search_term}+tutorial+beginners"),
            (f"Coursera: {clean_skill} Courses", f"https://www.coursera.org/search?query={search_term}"),
            (f"FreeCodeCamp: {clean_skill}", f"https://www.freecodecamp.org/news/search/?query={search_term}")
        ]

    return unique


def _extract_skills_from_text(text, role, field):
    """
    Extract structured skill items from aggregated web search text.
    Uses a comprehensive skill keyword dictionary to find relevant skills
    mentioned across multiple web sources.
    """
    text_lower = text.lower()

    # Comprehensive skill keyword bank organized by domain
    skill_bank = {
        # Programming Languages
        "python": "Python Programming",
        "java": "Java Programming",
        "javascript": "JavaScript",
        "c++": "C++ Programming",
        "c#": "C# Programming",
        "ruby": "Ruby Programming",
        "go": "Go (Golang)",
        "rust": "Rust Programming",
        "typescript": "TypeScript",
        "php": "PHP",
        "swift": "Swift Programming",
        "kotlin": "Kotlin",
        "r programming": "R Programming",

        # Data & Analytics
        "sql": "SQL & Database Querying",
        "excel": "Advanced Excel (Pivot Tables, VLOOKUP)",
        "power bi": "Power BI / Data Visualization",
        "tableau": "Tableau / Data Visualization",
        "statistics": "Statistics & Probability",
        "data analysis": "Data Analysis Fundamentals",
        "data visualization": "Data Visualization Tools",
        "pandas": "Python Pandas for Data Analysis",
        "numpy": "NumPy for Numerical Computing",

        # Machine Learning & AI
        "machine learning": "Machine Learning Algorithms",
        "deep learning": "Deep Learning (Neural Networks)",
        "tensorflow": "TensorFlow Framework",
        "pytorch": "PyTorch Framework",
        "nlp": "Natural Language Processing (NLP)",
        "computer vision": "Computer Vision",
        "artificial intelligence": "Artificial Intelligence Concepts",

        # Web Development
        "html": "HTML5 & Semantic Web",
        "css": "CSS3 & Responsive Design",
        "react": "React.js Frontend Framework",
        "angular": "Angular Framework",
        "vue": "Vue.js Framework",
        "node": "Node.js Backend",
        "django": "Django Web Framework",
        "flask": "Flask Web Framework",
        "spring": "Spring Boot (Java)",
        "rest api": "RESTful API Design",
        "api": "API Development & Integration",

        # DevOps & Cloud
        "docker": "Docker & Containerization",
        "kubernetes": "Kubernetes Orchestration",
        "aws": "Amazon Web Services (AWS)",
        "azure": "Microsoft Azure Cloud",
        "gcp": "Google Cloud Platform",
        "ci/cd": "CI/CD Pipelines",
        "devops": "DevOps Practices",
        "linux": "Linux Operating System",
        "git": "Version Control (Git & GitHub)",

        # Cyber Security
        "networking": "Networking Fundamentals",
        "ethical hacking": "Ethical Hacking & Pen Testing",
        "penetration testing": "Penetration Testing",
        "cryptography": "Cryptography",
        "firewall": "Firewall & Network Security",
        "security": "Cybersecurity Fundamentals",
        "siem": "SIEM Tools",

        # Design
        "figma": "Figma (UI/UX Design)",
        "adobe xd": "Adobe XD",
        "wireframing": "Wireframing & Prototyping",
        "user research": "User Research & Personas",
        "usability": "Usability Testing",

        # Soft Skills & General
        "data structures": "Data Structures & Algorithms",
        "algorithms": "Algorithms & Problem Solving",
        "system design": "System Design & Architecture",
        "agile": "Agile Methodology",
        "scrum": "Scrum Framework",
        "project management": "Project Management",
        "communication": "Communication Skills",
        "problem solving": "Problem Solving & Critical Thinking",
        "oop": "Object-Oriented Programming",
        "database": "Database Management",
        "testing": "Software Testing & QA",
        "automation": "Automation & Scripting",
    }

    # Count keyword occurrences in the web text
    found = {}
    for keyword, skill_name in skill_bank.items():
        count = text_lower.count(keyword)
        if count > 0:
            found[skill_name] = count

    if not found:
        return _fallback_skills(field, role)

    # Sort by frequency (most mentioned = most important)
    sorted_skills = sorted(found.items(), key=lambda x: x[1], reverse=True)

    # Take top 5-7 skills
    top_skills = [skill for skill, _ in sorted_skills[:7]]

    # Format as numbered roadmap steps
    roadmap = []
    for i, skill in enumerate(top_skills, 1):
        roadmap.append(f"{i}. {skill}")

    return roadmap


def _fallback_skills(field, role):
    """
    Fallback skill lists when web search returns no results.
    Uses broad domain-aware defaults.
    """
    field_lower = field.lower()
    role_lower = role.lower()

    if any(k in role_lower for k in ["data analyst", "analyst"]):
        return [
            "1. Advanced Excel (Pivot Tables, VLOOKUP, Macros)",
            "2. SQL Queries & Relational Databases",
            "3. Data Visualization (Tableau or Power BI)",
            "4. Python for Data Analysis (Pandas, NumPy)",
            "5. Statistics & Probability Fundamentals"
        ]
    elif any(k in role_lower for k in ["data scientist", "machine learning", "ml engineer"]):
        return [
            "1. Mathematics (Linear Algebra, Calculus, Statistics)",
            "2. Python Programming (Pandas, NumPy, Scikit-learn)",
            "3. SQL & Data Wrangling",
            "4. Machine Learning Algorithms",
            "5. Deep Learning (TensorFlow / PyTorch)",
            "6. Jupyter Notebooks & Git"
        ]
    elif any(k in role_lower for k in ["web developer", "frontend", "full stack"]):
        return [
            "1. HTML5 & Semantic Web",
            "2. CSS3 & Responsive Design (Flexbox, Grid)",
            "3. JavaScript (ES6+, DOM Manipulation)",
            "4. Frontend Framework (React.js or Vue.js)",
            "5. Backend Basics (Node.js or Django)",
            "6. Version Control (Git & GitHub)"
        ]
    elif any(k in role_lower for k in ["backend", "server"]):
        return [
            "1. Computer Science Fundamentals",
            "2. Programming Language (Python, Java, or Go)",
            "3. Databases & SQL (PostgreSQL, MySQL)",
            "4. RESTful API Design & HTTP",
            "5. Backend Frameworks (Spring Boot, Django, Express)",
            "6. Docker & Containerization"
        ]
    elif any(k in role_lower for k in ["software engineer", "software developer", "programmer"]):
        return [
            "1. Programming Fundamentals (CS50)",
            "2. Data Structures & Algorithms",
            "3. Object-Oriented Programming (OOP)",
            "4. Database Design (SQL & NoSQL)",
            "5. System Architecture & Design",
            "6. Version Control (Git) & CI/CD"
        ]
    elif any(k in role_lower for k in ["cyber", "security", "hacker", "penetration"]):
        return [
            "1. Networking Fundamentals (CompTIA Network+)",
            "2. Operating Systems (Linux, Windows)",
            "3. Security Fundamentals (CompTIA Security+)",
            "4. Scripting (Python & Bash)",
            "5. Ethical Hacking & Pen Testing Tools"
        ]
    elif any(k in role_lower for k in ["ui", "ux", "designer"]):
        return [
            "1. Principles of Visual Design & Color Theory",
            "2. User Research & Personas",
            "3. Wireframing & Information Architecture",
            "4. Prototyping Tools (Figma, Adobe XD)",
            "5. Usability Testing & Iteration"
        ]
    elif any(k in field_lower for k in ["data", "analytics"]):
        return [
            "1. Excel Proficiency",
            "2. Python or R Programming",
            "3. SQL for Data Querying",
            "4. Data Visualization Tools",
            "5. Statistical Analysis"
        ]
    else:
        return [
            "1. Core Industry Fundamentals",
            "2. Essential Software & Tooling",
            "3. Practical Project Building",
            "4. Problem Solving & Domain Theory",
            "5. Professional Communication Skills"
        ]
