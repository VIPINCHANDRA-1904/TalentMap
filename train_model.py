import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import os

def build_model():
    # Dataset according to user spec
    data = {
        "Skills": [
            "Python SQL Machine Learning Data Analysis Statistics",
            "Java Spring SQL Backend API",
            "HTML CSS JavaScript React Web Frontend",
            "Python SQL Power BI Statistics Excel Data Analysis",
            "Python Java C++ SQL Software Engineering Architecture"
        ],
        "Job Role": [
            "Data Scientist",
            "Backend Developer",
            "Web Developer",
            "Data Analyst",
            "Software Engineer"
        ]
    }
    df = pd.DataFrame(data)

    # Train a Machine Learning model that predicts best job role (Step 5)
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(df["Skills"], df["Job Role"])

    os.makedirs("models", exist_ok=True)
    with open("models/role_prediction_model.pkl", "wb") as f:
        pickle.dump(model, f)
        
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    build_model()
