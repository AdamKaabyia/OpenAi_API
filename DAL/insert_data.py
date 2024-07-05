import os
import sys
from dotenv import load_dotenv

# Add the path to the app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from DAL.models import db, QuestionAnswer

load_dotenv()

# Manually set the database URI if not set
database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if not database_uri:
    database_uri = "postgresql://postgres:mysecretpassword@localhost/your_database_name"

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.create_all()  # Ensure all tables are created

    # Create some sample data
    sample_questions = [
        {"question": "What is AI?", "answer": "AI is artificial intelligence."},
        {"question": "What is Python?", "answer": "Python is a programming language."}
    ]

    for item in sample_questions:
        new_entry = QuestionAnswer(question=item["question"], answer=item["answer"])
        db.session.add(new_entry)

    db.session.commit()

print("Sample data inserted successfully.")
