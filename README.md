# OpenAi_API


* OpenAi_API/
* │
* ├── DAL/
* │   ├── models.py
* │   ├── insert_data.py
* │
* ├── TEST/
* │   ├── request_response.py (tests api key separately)
* │   ├── test_app.py
* │
* ├── migrations/
* │   ├── versions/
* │   ├── alembic.ini
* │   ├── env.py
* │   ├── script.py.mako
* │
* ├── venv/
* │   ├── .dockerignore
* │   ├── .env
* │   ├── .gitignore
* │
* ├── app.py
* ├── docker-compose.yml
* ├── Dockerfile
* ├── entrypoint.sh
* ├── README.md
* ├── requirements.txt





# Set up the environment variables:
* Create a .env file in the root directory and add the following
SQLALCHEMY_DATABASE_URI=postgresql://postgres:mysecretpassword@db/your_database_name
OPENAI_KEY=your_openai_api_key


# Build and run the Docker containers:
docker-compose up --build

# Run the tests:
docker-compose run web pytest TEST/test_app.py
