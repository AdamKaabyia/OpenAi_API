import os
import pytest
import json
from app import app, db, QuestionAnswer


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def print_database():
    with app.app_context():
        questions = QuestionAnswer.query.all()
        for question in questions:
            print(f"ID: {question.id}, Question: {question.question}, Answer: {question.answer}")


def test_ask_endpoint(client):
    # Test first question
    response = client.post('/ask', data=json.dumps({'question': 'What is AI?'}), content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'answer' in data

    # Check the database for the first question
    with app.app_context():
        result = QuestionAnswer.query.filter_by(question='What is AI?').first()
        assert result is not None
        assert result.answer == data['answer']

    # Test new question
    question = 'who is jim carry'
    response = client.post('/ask', json={'question': question})
    data = response.json
    print(data['answer'])
    assert response.status_code == 200

    # Check the new question in the database
    with app.app_context():
        result = QuestionAnswer.query.filter_by(question=question).first()
        assert result is not None
        assert result.answer == data['answer']

    # Print the database contents
    print_database()


if __name__ == "__main__":
    os.environ['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mysecretpassword@localhost/your_database_name"
    pytest.main(["-s", "test_app.py"])
