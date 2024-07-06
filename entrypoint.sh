#!/bin/bash
# Wait for the database to be ready
echo "Waiting for DB to be ready..."
while ! pg_isready -h db -p 5432 -U postgres; do
    sleep 2
done

echo "Database is ready."

# Apply migrations
echo "Applying database migrations..."
flask db upgrade

# Check if we should initialize the database with sample data
if [ "$INIT_DB" = "true" ]; then
    echo "Initializing database with sample data..."
    python DAL/insert_data.py
fi

# Start the Flask application
echo "Starting Flask..."
flask run --host=0.0.0.0