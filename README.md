# Flask Todo App with Docker

This repository contains a simple Flask-based Todo application designed for containerised deployment with flexible database configuration.

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
- Docker (for containerised deployment)

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

### AWS ECS Deployment (Console Method)

#### Step 1: Push your Docker image to Amazon ECR

1. **Open the Amazon ECR console**: https://console.aws.amazon.com/ecr/
2. **Create a repository**:
   - Click "Create repository"
   - Name: `flask-todo-app`
   - Click "Create repository"
3. **View push commands**:
   - Select your new repository
   - Click "View push commands"
   - Follow the displayed commands to push your image

#### Step 2: Create an ECS Cluster

1. **Open the Amazon ECS console**: https://console.aws.amazon.com/ecs/
2. **Create a cluster**:
   - Click "Create Cluster"
   - Select "Networking only" (Fargate)
   - Name: `flask-todo-cluster`
   - Click "Create"

#### Step 3: Create a Task Definition

1. **Create task definition**:
   - In ECS console, go to "Task Definitions"
   - Click "Create new Task Definition"
   - Select "Fargate"
   - Click "Next step"

2. **Configure task**:
   - Task Definition Name: `flask-todo-task`
   - Task memory: `0.5GB`
   - Task CPU: `0.25 vCPU`

3. **Add container**:
   - Click "Add container"
   - Container name: `flask-todo-app`
   - Image: Your ECR image URI
   - Port mappings: `8080`
   - Environment variables (optional):
     - If using RDS: Add `DATABASE_URL` with your PostgreSQL connection string
   - Click "Add"
   - Click "Create"

#### Step 4: Create an ECS Service

1. **Create service**:
   - Go to your cluster
   - Click "Create"
   - Select "Service"
   - Launch type: `FARGATE`
   - Task Definition: Select your task definition
   - Service name: `flask-todo-service`
   - Number of tasks: `1`
   - Click "Next step"

2. **Configure network**:
   - Cluster VPC: Select your VPC
   - Subnets: Select at least two public subnets
   - Security groups: Create a new security group
     - Allow inbound on port 8080 from anywhere
   - Auto-assign public IP: `ENABLED`
   - Click "Next step"

3. **Set up load balancing**:
   - Load balancer type: `Application Load Balancer`
   - Create a new load balancer or use existing
   - Listener port: `80`
   - Target group name: `flask-todo-target`
   - Path pattern: `/`
   - Health check path: `/`
   - Click "Next step"

4. **Review and create**:
   - Review your settings
   - Click "Create Service"

#### Step 5: Access Your Application

1. Once the service is running, go to the "Load Balancers" section in EC2 console
2. Find your load balancer and copy the DNS name
3. Open the DNS name in your browser to access your Flask Todo App

#### Optional: Create an RDS Database

If you want to use PostgreSQL instead of SQLite:

1. **Open the RDS console**: https://console.aws.amazon.com/rds/
2. **Create database**:
   - Click "Create database"
   - Engine: `PostgreSQL`
   - Templates: `Free tier`
   - DB instance identifier: `flask-todo-db`
   - Master username: `postgres` (or your choice)
   - Master password: Create a secure password
   - DB instance class: `db.t3.micro`
   - VPC: Same as your ECS service
   - Security group: Create new, allow access from your ECS security group on port 5432
   - Initial database name: `tododb`
   - Click "Create database"

3. **Update your ECS task definition**:
   - Create a new revision of your task definition
   - Add the `DATABASE_URL` environment variable with your RDS connection string:
     ```
     postgresql://postgres:yourpassword@your-db-endpoint:5432/tododb
     ```
   - Update your service to use the new task definition

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

#### ECS Environment Variables
Environment variables are configured in the Task Definition. To update them:
1. Create a new revision of your task definition
2. Add or modify environment variables
3. Update your service to use the new task definition

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
