def map_role_to_career_field(role):
    mapping = {
        "Data Scientist": "Data Science",
        "Data Analyst": "Data Science",
        "Backend Developer": "Software Development",
        "Web Developer": "Web Development",
        "Software Engineer": "Software Development"
    }
    return mapping.get(role, "Technology")

def recommend_companies(role):
    """Returns list of company names for basic use (e.g. on interest results page)."""
    companies = {
        "Data Analyst": ["Deloitte", "Accenture", "TCS"],
        "Data Scientist": ["Google", "Amazon", "Meta"],
        "Backend Developer": ["Atlassian", "Oracle", "IBM"],
        "Web Developer": ["Amazon", "Flipkart", "Zoho"],
        "Software Engineer": ["Google", "Microsoft", "Infosys"]
    }
    return companies.get(role, ["TCS", "Infosys", "Wipro"])


def recommend_companies_detailed(role, match_score):
    """
    Returns detailed company profiles with:
    - Company name
    - Description of the role at that company
    - Hiring difficulty tier (affects selection chance)
    - Career page URL
    """
    company_db = {
        "Google": {
            "tier": "elite",  # Very competitive
            "career_url": "https://careers.google.com/",
            "descriptions": {
                "default": "Google hires top-tier engineers who can solve complex problems at massive scale. The role involves working on products used by billions, with a strong emphasis on data structures, algorithms, and system design.",
                "Data Scientist": "Google's Data Scientists work on search ranking, ad optimization, and YouTube recommendations. Requires strong ML fundamentals, statistical modeling, and experience with large-scale data pipelines.",
                "Software Engineer": "Google SWEs build infrastructure powering Search, Cloud, and Android. Requires deep knowledge of algorithms, distributed systems, and clean code practices."
            }
        },
        "Microsoft": {
            "tier": "elite",
            "career_url": "https://careers.microsoft.com/",
            "descriptions": {
                "default": "Microsoft offers roles across Azure, Office 365, Windows, and AI research. Engineers work on enterprise-scale products with global impact.",
                "Software Engineer": "Microsoft SWEs contribute to Azure cloud platform, VS Code, Teams, and AI services. Strong OOP, system design, and cloud knowledge are valued."
            }
        },
        "Amazon": {
            "tier": "high",
            "career_url": "https://www.amazon.jobs/",
            "descriptions": {
                "default": "Amazon hires across e-commerce, AWS, Alexa, and logistics. Roles focus on customer obsession, scalability, and leadership principles.",
                "Data Scientist": "Amazon Data Scientists optimize supply chain, pricing algorithms, and Alexa NLU. Requires expertise in ML, A/B testing, and big data tools.",
                "Web Developer": "Amazon Web Developers build high-traffic e-commerce interfaces and internal tools. Focus on React, performance optimization, and A/B testing."
            }
        },
        "Meta": {
            "tier": "elite",
            "career_url": "https://www.metacareers.com/",
            "descriptions": {
                "default": "Meta (Facebook) focuses on social networking, AR/VR, and the metaverse. Engineers work on products serving billions of daily active users.",
                "Data Scientist": "Meta Data Scientists analyze user engagement, ad performance, and content ranking. Requires SQL mastery, causal inference, and experiment design."
            }
        },
        "TCS": {
            "tier": "accessible",
            "career_url": "https://www.tcs.com/careers",
            "descriptions": {
                "default": "TCS is India's largest IT services company. Roles involve client-facing projects across banking, healthcare, and retail domains. Great for freshers and career starters.",
                "Data Analyst": "TCS Data Analysts work on client dashboards, reporting automation, and business intelligence projects using Excel, SQL, and Power BI."
            }
        },
        "Infosys": {
            "tier": "accessible",
            "career_url": "https://www.infosys.com/careers/",
            "descriptions": {
                "default": "Infosys provides digital transformation services globally. Known for structured training programs (Mysore campus). Excellent entry point for fresh graduates.",
                "Software Engineer": "Infosys SWEs work on enterprise Java, .NET, and cloud migration projects. The company invests heavily in upskilling through Infosys Springboard."
            }
        },
        "Wipro": {
            "tier": "accessible",
            "career_url": "https://careers.wipro.com/",
            "descriptions": {
                "default": "Wipro offers IT consulting and services across multiple industry verticals. Known for its diverse project portfolio and strong training programs.",
            }
        },
        "Deloitte": {
            "tier": "high",
            "career_url": "https://www.deloitte.com/careers",
            "descriptions": {
                "default": "Deloitte is a Big Four firm with strong analytics and consulting practices. Roles combine business acumen with technical skills.",
                "Data Analyst": "Deloitte Data Analysts work on consulting engagements, building client dashboards, financial models, and business intelligence solutions using Tableau, SQL, and Python."
            }
        },
        "Accenture": {
            "tier": "moderate",
            "career_url": "https://www.accenture.com/careers",
            "descriptions": {
                "default": "Accenture is a global consulting and technology services leader. Offers diverse projects across AI, cloud, security, and digital transformation.",
                "Data Analyst": "Accenture Data Analysts support enterprise clients with data-driven decision making, using tools like Power BI, Alteryx, and SQL across various industries."
            }
        },
        "Atlassian": {
            "tier": "high",
            "career_url": "https://www.atlassian.com/company/careers",
            "descriptions": {
                "default": "Atlassian builds collaboration tools like Jira, Confluence, and Trello. Engineering culture emphasizes remote work, innovation, and team autonomy.",
                "Backend Developer": "Atlassian Backend Developers build scalable microservices for Jira Cloud and Confluence. Tech stack includes Java, Kotlin, AWS, and event-driven architectures."
            }
        },
        "Oracle": {
            "tier": "high",
            "career_url": "https://www.oracle.com/careers/",
            "descriptions": {
                "default": "Oracle is a leader in database technology and enterprise cloud. Engineers work on Oracle Cloud Infrastructure (OCI), database kernels, and enterprise apps.",
                "Backend Developer": "Oracle Backend Developers work on cloud infrastructure, database engines, and enterprise middleware. Strong Java and distributed systems knowledge required."
            }
        },
        "IBM": {
            "tier": "moderate",
            "career_url": "https://www.ibm.com/careers",
            "descriptions": {
                "default": "IBM focuses on hybrid cloud, AI (Watson), and quantum computing. Offers structured career paths and strong research opportunities.",
                "Backend Developer": "IBM Backend Developers work on Watson AI services, Red Hat OpenShift, and enterprise cloud solutions. Python, Java, and Kubernetes expertise valued."
            }
        },
        "Flipkart": {
            "tier": "high",
            "career_url": "https://www.flipkartcareers.com/",
            "descriptions": {
                "default": "Flipkart is India's leading e-commerce platform. Engineers tackle high-scale challenges in supply chain, payments, and personalization.",
                "Web Developer": "Flipkart Web Developers build the shopping experience for millions of users. Focus on React, performance optimization, mobile-first design, and handling flash sales at massive scale."
            }
        },
        "Zoho": {
            "tier": "moderate",
            "career_url": "https://www.zoho.com/careers.html",
            "descriptions": {
                "default": "Zoho is a product-based company building 50+ business apps. Known for building everything in-house without external funding.",
                "Web Developer": "Zoho Web Developers work on SaaS products like Zoho CRM, Mail, and Creator. The company uses its own frameworks and values deep engineering skills over framework trends."
            }
        }
    }

    # Get base company names for this role
    base_companies = recommend_companies(role)

    detailed_list = []
    for company_name in base_companies:
        info = company_db.get(company_name, {})
        tier = info.get("tier", "moderate")
        career_url = info.get("career_url", f"https://www.google.com/search?q={company_name}+careers")

        # Get role-specific description or fallback to default
        descriptions = info.get("descriptions", {})
        description = descriptions.get(role, descriptions.get("default", f"{company_name} is actively hiring for {role} positions. Visit their careers page for more details."))

        # Calculate selection chance based on match_score + company tier
        selection_chance = _calculate_selection_chance(match_score, tier)

        detailed_list.append({
            "name": company_name,
            "description": description,
            "selection_chance": selection_chance,
            "career_url": career_url,
            "tier": tier
        })

    return detailed_list


def _calculate_selection_chance(match_score, tier):
    """
    Estimate selection chance based on candidate match score and company competitiveness.
    """
    tier_multipliers = {
        "elite": 0.55,      # Very competitive (Google, Meta, Microsoft)
        "high": 0.70,       # Competitive (Amazon, Atlassian, Flipkart)
        "moderate": 0.85,   # Moderately competitive (Accenture, IBM, Zoho)
        "accessible": 0.95  # More accessible (TCS, Infosys, Wipro)
    }

    multiplier = tier_multipliers.get(tier, 0.80)
    raw_chance = match_score * multiplier * 0.9

    # Clamp between 15% and 85%
    return max(15, min(85, round(raw_chance)))


def get_required_skills(role):
    # Normalize input
    role_lower = role.lower()
    
    req_skills = {
        "data analyst": [
            "1. Advanced Excel (Pivot tables, VLOOKUP)", 
            "2. SQL Queries & Relational Databases", 
            "3. Data Visualization (Tableau or Power BI)", 
            "4. Python for Data Analysis (Pandas, NumPy)", 
            "5. Basic Statistics & Probability"
        ],
        "data scientist": [
            "1. Foundational Math (Linear Algebra, Calc, Stats)",
            "2. Python (Pandas, NumPy, Scikit-Learn)",
            "3. SQL & Data Wrangling",
            "4. Core Machine Learning Algorithms",
            "5. Deep Learning (TensorFlow or PyTorch)",
            "6. Jupyter Notebooks & Git"
        ],
        "backend developer": [
            "1. CS50 / Computer Science Fundamentals",
            "2. Programming Basics (Python, Java, or Node.js)", 
            "3. Relational Databases & SQL (PostgreSQL, MySQL)", 
            "4. RESTful API Design & HTTP",
            "5. Backend Frameworks (Spring Boot, Django, or Express)", 
            "6. Docker & Containerization basics"
        ],
        "web developer": [
            "1. How the Internet Works (HTTP, DNS)",
            "2. HTML5 & Semantic Web", 
            "3. CSS3 & Responsive Design (Flexbox, Grid)", 
            "4. Modern JavaScript (ES6+ & DOM Manipulation)", 
            "5. Frontend Framework (React.js or Vue)", 
            "6. Version Control (Git & GitHub)"
        ],
        "software engineer": [
            "1. CS50 & Programming Fundamentals", 
            "2. Data Structures & Algorithms", 
            "3. Object-Oriented Programming (OOP)",
            "4. Database Design (SQL & NoSQL)", 
            "5. System Architecture & System Design",
            "6. Version Control (Git) & CI/CD Pipelines"
        ],
        "cyber security": [
            "1. Networking Fundamentals (CompTIA Network+ / CCNA)", 
            "2. Operating Systems Deep Dive (Linux, Windows)", 
            "3. Security Fundamentals (CompTIA Security+)", 
            "4. Scripting (Python & Bash)", 
            "5. Ethical Hacking & Penetration Testing Tools"
        ],
        "ui/ux": [
            "1. Principles of Design & Color Theory", 
            "2. User Research & Personas", 
            "3. Wireframing & Information Architecture", 
            "4. Prototyping Tools (Figma or Adobe XD)", 
            "5. Usability Testing & Iteration"
        ]
    }
    
    for key in req_skills:
        if key in role_lower:
            return req_skills[key]
            
    # Intelligent fallback for unknown roles
    if "developer" in role_lower or "engineer" in role_lower or "programmer" in role_lower:
        return [
            "1. Computer Science Fundamentals (CS50)",
            "2. Object-Oriented Programming Language (Python, Java, C++)", 
            "3. Version Control (Git & GitHub)", 
            "4. Database Management & SQL", 
            "5. Data Structures & Algorithms",
            "6. Project Building & System Design"
        ]
    elif "data" in role_lower or "analyst" in role_lower:
        return [
            "1. Spreadsheet Prowess (Excel)",
            "2. Scripting Language (Python or R)", 
            "3. Database querying (SQL)", 
            "4. Data Visualization Tools", 
            "5. Basic Statistical Analysis"
        ]
    
    return [
        "1. Core Industry Fundamentals", 
        "2. Essential Software & Tooling", 
        "3. Practical Project Building", 
        "4. Problem Solving & Theory", 
        "5. Networking & Communication Skills"
    ]

def get_learning_resources(skill):
    resources = {
        "cs50": [
            ("Harvard CS50 Full Course (YouTube)", "https://www.youtube.com/watch?v=8mAITcNt710"),
            ("edX Complete CS50 Platform", "https://www.edx.org/course/introduction-computer-science-harvardx-cs50x")
        ],
        "python": [
            ("Programming with Mosh - Python for Beginners", "https://www.youtube.com/watch?v=_uQrJ0TkZlc"),
            ("FreeCodeCamp Python Course", "https://www.youtube.com/watch?v=rfscVS0vtbw"),
            ("Corey Schafer Python Tutorials", "https://www.youtube.com/user/schafer5")
        ],
        "sql": [
            ("Mode SQL Tutorial (Interactive)", "https://mode.com/sql-tutorial/"),
            ("FreeCodeCamp SQL Full Course", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
            ("SQLBolt - Learn SQL visually", "https://sqlbolt.com/")
        ],
        "javascript": [
            ("Traversy Media JavaScript Crash Course", "https://www.youtube.com/watch?v=hdI2bqOjy3c"),
            ("MDN Web Docs JS Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
            ("FreeCodeCamp JS Data Structures", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")
        ],
        "java": [
            ("Bro Code Java Full Course", "https://www.youtube.com/watch?v=xk4_1vDrzzo"),
            ("Mooc.fi Object Oriented Programming", "https://java-programming.mooc.fi/"),
            ("Amigoscode Java Tutorial", "https://www.youtube.com/watch?v=A74TOX803D0")
        ],
        "c++": [
            ("The Cherno C++ Series (YouTube)", "https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUjcMTc7k0_sN"),
            ("LearnCpp.com", "https://www.learncpp.com/"),
            ("FreeCodeCamp C++ For Beginners", "https://www.youtube.com/watch?v=vLnPwxZdW4Y")
        ],
        "machine learning": [
            ("Andrew Ng Machine Learning (Coursera)", "https://www.coursera.org/specializations/machine-learning-introduction"),
            ("StatQuest with Josh Starmer", "https://www.youtube.com/user/joshstarmer"),
            ("Kaggle Micro-courses (Interactive)", "https://www.kaggle.com/learn")
        ],
        "deep learning": [
            ("Fast.ai - Practical Deep Learning", "https://course.fast.ai/"),
            ("3Blue1Brown Neural Networks", "https://www.youtube.com/watch?v=aircAruvnKk"),
            ("DeepLearning.AI (Coursera)", "https://www.coursera.org/specializations/deep-learning")
        ],
        "react": [
            ("React Official Documentation", "https://react.dev/learn"),
            ("Codevolution React Course", "https://www.youtube.com/watch?v=QFaFIcZ05iU&list=PLC3y8-rFHvwgg3vaYJgHGnModB54rxOk3"),
            ("Web Dev Simplified React Hooks", "https://www.youtube.com/watch?v=O6P86uwfdR0&list=PLZlA0Gpn_vH8EtcCoxPXPCXRoXIRoLUo")
        ],
        "power bi": [
            ("Kevin Stratvert Power BI Tutorial", "https://www.youtube.com/watch?v=TmhQCQr_DCA"),
            ("Microsoft Learn Platform", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi")
        ],
        "excel": [
            ("Leila Gharani Advanced Excel", "https://www.youtube.com/c/LeilaGharani"),
            ("Excel Campus", "https://www.excelcampus.com/")
        ],
        "html": [
            ("Kevin Powell Web Design Basics", "https://www.youtube.com/user/KepowOb"),
            ("FreeCodeCamp Responsive Web Design", "https://www.freecodecamp.org/learn/responsive-web-design/")
        ],
        "css": [
            ("CSS-Tricks", "https://css-tricks.com/"),
            ("Web Dev Simplified CSS Flexbox/Grid", "https://www.youtube.com/watch?v=fYq5PXgSsbE")
        ],
        "algorithms": [
            ("NeetCode (LeetCode Solutions)", "https://www.youtube.com/c/NeetCode"),
            ("Abdul Bari Algorithms Course", "https://www.youtube.com/watch?v=0IAPZzGSbME&list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O"),
            ("Grokking Algorithms (Book)", "https://www.manning.com/books/grokking-algorithms")
        ],
        "system": [
            ("ByteByteGo System Design", "https://www.youtube.com/c/ByteByteGo"),
            ("Gaurav Sen System Design", "https://www.youtube.com/c/GauravSensei"),
            ("System Design Interview", "https://github.com/donnemartin/system-design-primer")
        ],
        "git": [
            ("Programming with Mosh Git Tutorial", "https://www.youtube.com/watch?v=8JJ101D3knE"),
            ("Atlassian Git Tutorial", "https://www.atlassian.com/git/tutorials")
        ],
        "networking": [
            ("NetworkChuck - Free CCNA", "https://www.youtube.com/watch?v=q6yIs0r2eGU&list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P"),
            ("Professor Messer Network+", "https://www.youtube.com/user/professormesser")
        ],
        "security": [
            ("The Cyber Mentor", "https://www.youtube.com/c/TheCyberMentor"),
            ("TryHackMe (Interactive Learning)", "https://tryhackme.com/")
        ],
        "figma": [
            ("Figma In 40 Minutes", "https://www.youtube.com/watch?v=jwLlTEApKjc"),
            ("DesignCourse UI/UX", "https://www.youtube.com/user/DesignCourse")
        ]
    }
    
    skill_lower = skill.lower()
    
    # Try finding multi-word overlap
    for key, val in resources.items():
        if key in skill_lower:
            return val
            
    # Default fallback utilizing youtube search precisely crafted
    clean_search = skill.split('.')[1].strip() if '.' in skill else skill
    return [
        (f"Watch Beginner Tutorials for {clean_search}", f"https://www.youtube.com/results?search_query=best+tutorial+for+{clean_search.replace(' ', '+')}+beginners"),
        (f"Coursera Certifications for {clean_search}", f"https://www.coursera.org/search?query={clean_search.replace(' ', '+')}"),
        (f"FreeCodeCamp Guides for {clean_search}", f"https://www.freecodecamp.org/news/search/?query={clean_search.replace(' ', '+')}")
    ]

def detect_skill_gap(candidate_skills, required_skills):
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    candidate_text = " ".join(candidate_skills_lower)
    missing = []
    for req in required_skills:
        req_lower = req.lower()
        # Check exact match first
        if req_lower in candidate_skills_lower:
            continue
        # Check partial/keyword overlap (e.g. "Python" matches "Python Programming")
        req_words = req_lower.split()
        if any(word in candidate_text for word in req_words if len(word) > 2):
            continue
        missing.append(req)
    return missing

def calculate_match_score(candidate_skills, required_skills):
    """
    Calculate a fair match score that considers:
    1. Exact skill matches
    2. Partial/related skill matches (e.g. 'python' partially matches 'data analysis with python')
    3. A base confidence boost (every candidate with skills gets some credit)
    
    This avoids overly harsh scores that would demotivate candidates.
    Formula inspired by real ATS systems.
    """
    if not required_skills:
        return 0
    if not candidate_skills:
        return 15  # Even uploading a resume shows initiative
    
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    candidate_text = " ".join(candidate_skills_lower)
    
    exact_matches = 0
    partial_matches = 0
    
    for req in required_skills:
        req_lower = req.lower()
        if req_lower in candidate_skills_lower:
            exact_matches += 1
        else:
            # Check for partial/keyword overlap
            req_words = req_lower.split()
            if any(word in candidate_text for word in req_words if len(word) > 2):
                partial_matches += 1
    
    total_required = len(required_skills)
    
    # Weighted scoring: exact matches worth full marks, partial matches worth half
    weighted_score = (exact_matches + (partial_matches * 0.5)) / total_required
    
    # Base confidence: having any skills at all gets a minimum of 25%
    base_confidence = min(25, len(candidate_skills) * 5)
    
    # Final score: base + weighted (capped at 95 to leave room for improvement)
    raw_score = base_confidence + (weighted_score * 70)
    final_score = min(95, max(20, round(raw_score)))
    
    return final_score
