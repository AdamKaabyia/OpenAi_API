import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
from DAL.models import db, QuestionAnswer
from TEST.request_response import get_openai_response

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/ask', methods=['POST'])
def ask():
    if not request.is_json:
        return jsonify({"error": "Invalid data format: please provide JSON data"}), 400

    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer, error = get_openai_response(question)
    if error:
        return jsonify({"error": answer}), 500

    try:
        new_entry = QuestionAnswer(question=question, answer=answer)
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database transaction failed: " + str(e)}), 500

    return jsonify({"question": question, "answer": answer})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
