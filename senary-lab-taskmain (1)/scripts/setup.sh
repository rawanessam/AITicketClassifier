#!/bin/bash

# Setup script for the IT Support Ticket System

echo "🚀 Setting up IT Support Ticket System..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration values"
    echo "   Especially set your OPENAI_API_KEY"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/ticket_data
mkdir -p frontend/dist

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test backend health
echo "🏥 Testing backend health..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend is not responding"
fi

# Test frontend
echo "🌐 Testing frontend..."
if curl -f http://localhost:3000/ > /dev/null 2>&1; then
    echo "✅ Frontend is running successfully"
else
    echo "❌ Frontend is not responding"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Service URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Full Application: http://localhost (via nginx)"
echo "   Database: localhost:5432"
echo ""
echo "📖 Useful commands:"
echo "   View logs: make logs"
echo "   Stop services: make down"
echo "   Restart: make restart"
echo "   Development mode: make dev"
echo ""
echo "⚠️  Don't forget to configure your .env file with proper values!"
