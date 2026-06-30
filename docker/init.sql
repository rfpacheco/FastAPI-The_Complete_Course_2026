-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    phone_number VARCHAR(20)
);

-- Create todos table
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    complete BOOLEAN DEFAULT FALSE,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_todos_owner_id ON todos(owner_id);

-- Insert sample users with hashed passwords (bcrypt hashed versions)
-- These are hashed versions for testing purposes
INSERT INTO users (email, username, first_name, last_name, hashed_password, is_active, role, phone_number)
VALUES
    ('john.doe@example.com', 'johndoe', 'John', 'Doe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm', TRUE, 'admin', '+1-555-0101'),
    ('jane.smith@example.com', 'janesmith', 'Jane', 'Smith', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm', TRUE, 'user', '+1-555-0102'),
    ('bob.wilson@example.com', 'bobwilson', 'Bob', 'Wilson', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm', TRUE, 'user', '+1-555-0103')
ON CONFLICT (email) DO NOTHING;

-- Insert sample todos
INSERT INTO todos (title, description, priority, complete, owner_id)
VALUES
    ('Learn FastAPI', 'Complete the FastAPI course and build a production app', 1, FALSE, 1),
    ('Set up PostgreSQL', 'Configure PostgreSQL database with Docker', 1, TRUE, 1),
    ('Create API endpoints', 'Design and implement RESTful API endpoints', 2, FALSE, 1),
    ('Write unit tests', 'Write comprehensive tests for all endpoints', 2, FALSE, 2),
    ('Deploy to production', 'Set up CI/CD and deploy application', 3, FALSE, 1),
    ('Bug fixes', 'Fix reported issues from beta testing', 2, FALSE, 2),
    ('Code review', 'Review team members code and provide feedback', 3, FALSE, 3),
    ('Documentation', 'Write comprehensive API documentation', 2, FALSE, 3)
ON CONFLICT DO NOTHING;
