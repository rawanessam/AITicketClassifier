-- Initialize the ticket system database
CREATE DATABASE IF NOT EXISTS ticket_system;

-- Create tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    ticket_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    issue_description TEXT NOT NULL,
    feedback_text TEXT,
    category VARCHAR(50),
    urgency_score INTEGER,
    attachments JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on ticket_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_ticket_id ON tickets(ticket_id);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_created_at ON tickets(created_at);

-- Create index on category for filtering
CREATE INDEX IF NOT EXISTS idx_category ON tickets(category);

-- Create index on urgency_score for prioritization
CREATE INDEX IF NOT EXISTS idx_urgency_score ON tickets(urgency_score);
