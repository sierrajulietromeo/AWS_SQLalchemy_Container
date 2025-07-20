# Flask Todo App with Docker

This repository contains a simple Flask-based Todo application designed for containerized deployment with flexible database configuration.

## Features

- Add, view, and delete tasks with priorities
- Uses SQLAlchemy ORM for database operations
- Configurable database backend:
  - Uses `DATABASE_URL` environment variable if set (supports PostgreSQL, MySQL, etc.)
  - Defaults to SQLite for local development

## Database Configuration

The application automatically detects and uses the appropriate database:

- **Production**: Set `DATABASE_URL` environment variable
  - PostgreSQL: `postgresql://user:password@host:port/dbname`
  - MySQL: `mysql://user:password@host:port/dbname`
- **Local Development**: Defaults to SQLite (`sqlite:///todo.db`) if no `DATABASE_URL` is set

## Getting Started

### Prerequisites

- Python 3.x (for local development)
- Docker (for containerized deployment)

### Local Development

1. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) Create a `.env` file for local database configuration:
    ```bash
    # For local PostgreSQL
    DATABASE_URL=postgresql://user:password@localhost:5432/todo_local
    
    # Or leave blank to use SQLite (default)
    ```

4. Run the application:
    ```bash
    python application.py
    ```

The app will be available at `http://localhost:8080`

### Docker Deployment

#### Building the Docker Image

```bash
docker build -t flask-todo-app .
```

#### Running the Container

With SQLite (default):
```bash
docker run -p 8080:8080 flask-todo-app
```

With PostgreSQL:
```bash
docker run -p 8080:8080 -e DATABASE_URL=postgresql://user:password@host:port/dbname flask-todo-app
```

### Environment Variable Configuration

#### Local Development (.env file)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/todo_dev
```

#### Docker Environment Variables
```bash
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:password@host:port/dbname \
  flask-todo-app
```

## Project Structure

```
.
├── application.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── index.html
│   └── tasks.html
├── static/                 # Static assets
│   └── style.css
├── Dockerfile              # Docker configuration
├── .env                    # Local environment variables (optional)
└── README.md
```

## Database Schema

The application uses SQLAlchemy models:

- **Task Table**:
  - `id`: Primary key (Integer)
  - `task`: Task description (String, max 255 chars)
  - `priority`: Task priority (Integer, default: 1)

Database tables are automatically created on first run.

## Notes

- The application uses SQLAlchemy ORM for database operations, making it database-agnostic
- Database tables are created automatically when the application starts
- For production deployments, use PostgreSQL or MySQL for better performance and reliability
- SQLite is suitable for development and testing only
- Remember to add `.env` to your `.gitignore` if storing sensitive database credentials locally