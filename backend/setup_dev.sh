#!/bin/bash

# Development setup script for MaplePath FastAPI backend

echo "Setting up MaplePath FastAPI backend for development..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment (Linux/Mac)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
# Activate virtual environment (Windows)
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update the .env file with your database credentials and Firebase config"
fi

# Initialize Alembic (create initial migration)
echo "Initializing database migrations..."
alembic init migrations

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your database URL and Firebase credentials"
echo "2. Create your PostgreSQL database"
echo "3. Run: alembic revision --autogenerate -m 'Initial migration'"
echo "4. Run: alembic upgrade head"
echo "5. Start development server: uvicorn main:app --reload"
