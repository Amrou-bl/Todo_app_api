# Todo App API

## Description
A simple Todo application built with FastAPI, Docker, and PostgreSQL. This application allows users to manage their tasks with authentication and authorization, enabling users to create, read, update, and delete their todo items securely.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-app-api.git
   cd todo-app-api
2. Make sure you have Docker and Docker Compose installed.
3. Build and run the application:
   ```bash
   docker-compose up --build
4. The application will be available at:
   * Authentication Service: http://localhost:8000/auth
   * *Todo Service: http://localhost:8001/todos
     
## Usage

After running the application, you can use the following API endpoints to interact with the Todo app.
API Endpoints

   * Authentication Service:
        POST /auth/login - Authenticate a user and get a token.
        POST /auth/register - Register a new user.
   * Todo Service:
        GET /todos - Get all todos (requires authentication).
        POST /todos - Create a new todo (requires authentication).
        PUT /todos/{id} - Update a todo by ID (requires authentication).
        DELETE /todos/{id} - Delete a todo by ID (requires authentication).

        
