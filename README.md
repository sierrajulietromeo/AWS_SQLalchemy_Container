# Flask Todo App for AWS Elastic Beanstalk

This repository contains a simple Flask-based Todo application designed for deployment on AWS Elastic Beanstalk with flexible database configuration.

## Features

- Add, view, and delete tasks with priorities
- Uses SQLAlchemy ORM for database operations
- Configurable database backend:
  - Uses `DATABASE_URL` environment variable if set (supports PostgreSQL, MySQL, etc.)
  - Defaults to SQLite for local development
- Ready for deployment on Elastic Beanstalk with RDS integration

## Database Configuration

The application automatically detects and uses the appropriate database:

- **Production (Elastic Beanstalk + RDS)**: Set `DATABASE_URL` environment variable
  - PostgreSQL: `postgresql://user:password@host:port/dbname`
  - MySQL: `mysql://user:password@host:port/dbname`
- **Local Development**: Defaults to SQLite (`sqlite:///todo.db`) if no `DATABASE_URL` is set

## Getting Started

### Prerequisites

- Python 3.x

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

### Deploying to Elastic Beanstalk

#### Option 1: Using RDS (Recommended)

1. Create an RDS instance (PostgreSQL or MySQL recommended)

2. Set the `DATABASE_URL` environment variable in Elastic Beanstalk:
   - **Via EB Console**: Configuration → Software → Environment variables
   - **Via EB CLI**: `eb setenv DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dbname`
   - **Via .ebextensions**: Add to your configuration files

3. Zip your project files and deploy:
    ```bash
    # Include these files in your zip
    application.py
    requirements.txt
    templates/
    .ebextensions/
    ```

4. Upload via AWS Elastic Beanstalk console

#### Option 2: Using SQLite (Not recommended for production)

- Deploy without setting `DATABASE_URL` - the app will use SQLite
- Note: SQLite files are not persistent across deployments in EB

### Environment Variable Configuration

#### Local Development (.env file)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/todo_dev
```

#### Elastic Beanstalk Environment Variables
Set via EB Console, CLI, or `.ebextensions/database.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DATABASE_URL: postgresql://user:password@your-rds-endpoint:5432/dbname
```

## Project Structure

```
.
├── application.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/             # HTML templates
│   ├── index.html
│   └── tasks.html
├── .ebextensions/         # EB configuration
│   └── flask.config
├── .env                   # Local environment variables (optional)
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
- For production deployments, use RDS with PostgreSQL or MySQL for better performance and reliability
- SQLite is suitable for development and testing only
- Remember to add `.env` to your `.gitignore` if storing sensitive database credentials locally