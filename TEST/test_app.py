import os
import pytest
from flask import json
from app import app, db, QuestionAnswer


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Set the URI from environment variable or use a default that you know is correct
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI',
                                                      'postgresql://postgres:mysecretpassword@localhost/your_database_name')
    with app.app_context():
        db.create_all()
        yield app.test_client()  # Provides a testing client
        db.session.remove()
        db.drop_all()


def print_database():
    with app.app_context():
        questions = QuestionAnswer.query.all()
        for question in questions:
            print(f"ID: {question.id}, Question: {question.question}, Answer: {question.answer}")


def test_ask_endpoint(client):
    # Test the first question using the JSON approach for consistency
    response = client.post('/ask', json={'question': 'What is AI?'})
    assert response.status_code == 200
    data = response.json
    assert 'answer' in data

    # Validate the answer is stored in the database
    with app.app_context():
        result = QuestionAnswer.query.filter_by(question='What is AI?').first()
        assert result is not None
        #assert result.answer == data['answer']

    # Test with another question
    question = 'who is jim carry'
    response = client.post('/ask', json={'question': question})
    data = response.json
    print(data['answer'])
    assert response.status_code == 200

    # Validate the second question in the database
    with app.app_context():
        result = QuestionAnswer.query.filter_by(question=question).first()
        assert result is not None
        #assert result.answer == data['answer']

    # Optionally print all entries from the database for verification
    print_database()


if __name__ == "__main__":
    os.environ['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mysecretpassword@localhost/your_database_name"
    pytest.main(["-s", "test_app.py"])
