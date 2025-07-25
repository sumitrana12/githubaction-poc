# Flask Message Board with DevSecOps Pipeline

A Flask-based message board application with a comprehensive DevSecOps pipeline for building and deploying Docker images. This project demonstrates modern CI/CD practices with a focus on security, testing, and environment-based deployments.

## Application Features

- **Message Board**: Simple and elegant interface for posting and viewing messages
- **RESTful API**: Backend API for programmatic interaction with the message board
- **Persistent Storage**: SQLite database for reliable message storage
- **Health Monitoring**: Endpoint for system health checks and monitoring
- **Responsive Design**: Mobile-friendly web interface
- **Environment-Aware**: Configuration adapts to development, staging, and production

## Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized deployment)

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt

# Run the application
python src/run.py
```

The application will be available at [http://localhost:5000](http://localhost:5000)

### Docker Deployment

```bash
# Build the image
docker build -t sumitrana/flask-message-board:latest .

# Run the container
docker run -p 5000:5000 sumitrana/flask-message-board:latest
```

## Using the Application

### Web Interface

1. **Access the Application**: Navigate to [http://localhost:5000](http://localhost:5000)
2. **View Messages**: All existing messages appear on the main page
3. **Post a Message**: Type your message in the text area and click "Post Message"

### API Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/messages` | GET | Retrieve all messages | None | JSON array of messages |
| `/api/messages` | POST | Create a new message | `{"content": "Your message"}` | Created message object |
| `/api/health` | GET | Check application health | None | Health status object |

#### Example API Usage

**Get Messages**
```bash
curl -X GET http://localhost:5000/api/messages
```

**Create Message**
```bash
curl -X POST http://localhost:5000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from the API!"}'
```

**Check Health**
```bash
curl -X GET http://localhost:5000/api/health
```

## Project Structure

```
.
├── src/                      # Application source code
│   ├── app/                  # Flask application package
│   │   ├── __init__.py       # Application initialization
│   │   ├── models.py         # Database models
│   │   ├── views.py          # Route handlers
│   │   └── templates/        # HTML templates
│   │       └── index.html    # Main page template
│   ├── tests/                # Test files
│   │   ├── __init__.py       # Makes tests a package
│   │   └── test_app.py       # Test cases for app
│   ├── data/                 # Database storage
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Application entry point
├── Dockerfile                # Multi-stage Docker build file
├── .dockerignore             # Files to ignore in Docker build
└── .github/workflows/        # GitHub Actions workflows
    └── devsecops-pipeline.yml  # Main DevSecOps pipeline
```

## Architecture

This application follows a simple MVC (Model-View-Controller) architecture:

- **Models** (`src/app/models.py`): Handles database operations and data structure
- **Views** (`src/app/templates/`): HTML templates for the user interface
- **Controllers** (`src/app/views.py`): Route handlers for processing requests

The SQLite database is used for data persistence and is stored in the `src/data` directory.

## Branch-Based Deployment Strategy

This project uses a branch-based deployment strategy:

| Branch | Environment | Image Tag      | Description                        |
|--------|------------|-----------------|-----------------------------------|
| `main` | Production | `prod`          | Production-ready, stable code      |
| `stage`| Staging    | `staging`       | Pre-production testing environment |
| `dev`  | Development| `dev`           | Development and integration testing|

Each branch automatically deploys to its corresponding environment when changes are pushed.

## DevSecOps Pipeline

Our optimized pipeline includes the following stages:

1. **Validate and Test**
   - Code linting with Flake8 (only fails on critical errors)
   - SAST scanning with Bandit (fails on any high issues or >5 medium issues)
   - Dependency scanning with Safety (configurable severity thresholds)
   - Unit testing with pytest and coverage reporting

2. **Build, Scan, and Push**
   - Single-stage process for efficiency 
   - Multi-stage Docker build for smaller images
   - Container scanning with Trivy
   - Dual tagging strategy:
     - Environment tag (e.g., `dev`, `staging`, `prod`)
     - Timestamped tag (e.g., `dev-20250725-153045`)

3. **Deploy**
   - Environment-specific configuration and secrets
   - Zero-downtime deployment strategy

4. **Security Audit**
   - Dynamic Application Security Testing
   - Compliance verification

5. **Post-Deployment**
   - Automated smoke tests
   - Team notifications

### Pipeline Optimizations

- **Single Docker build**: Builds once and reuses the image for scanning and pushing
- **Timestamp-based versioning**: Creates immutable artifact history for each build
- **Configurable security thresholds**: Different severity levels for different security tools
- **Enhanced logging**: Clear status messages throughout the pipeline
- **Artifact reuse**: Shares built artifacts between jobs for efficiency

The pipeline dynamically determines the target environment and image tags based on the branch name, and uses GitHub artifacts to pass code between jobs, avoiding redundant checkouts.

## Security Features

- **Multi-stage Docker builds**: Minimizes attack surface and image size
- **Non-root user in container**: Reduces risk of container escape vulnerabilities
- **SAST (Static Application Security Testing)**: Identifies security issues in code
- **Dependency scanning**: Checks for vulnerabilities in dependencies
- **Container vulnerability scanning**: Detects OS-level vulnerabilities
- **DAST (Dynamic Application Security Testing)**: Tests running application security
- **Proper data volume management**: Secures persistent data
- **Healthcheck implementation**: Ensures application availability
- **Input validation**: Prevents injection attacks
- **Environment-based configuration**: Isolates environments for better security
- **Configurable security thresholds**: Different policies for different severity levels

## Setup Requirements for CI/CD

To use this workflow, you need to add the following secrets to your GitHub repository environments (development, staging, and production):

1. `DOCKER_USERNAME` - Your Docker Hub username
2. `DOCKER_TOKEN` - Your Docker Hub access token (not your password)

You'll need to create three environments in your GitHub repository settings:
- `development`
- `staging`
- `production`

## Extending the Application

Here are some ideas for extending this application:

1. **User Authentication**: Add user registration and login
2. **Message Management**: Allow editing and deleting messages
3. **Categories/Tags**: Organize messages by topics
4. **Rich Content**: Support markdown or formatting in messages
5. **File Attachments**: Allow users to upload images or files
6. **Pagination**: Add support for paged message display
7. **Search**: Implement message search functionality
8. **Real-time Updates**: Add websockets for live message updates
9. **User Profiles**: Add user profile information and avatars
10. **Admin Panel**: Create an administrative interface for moderation

## Testing

Run the tests with:

```bash
cd src
pytest tests/
```

Generate a coverage report:

```bash
cd src
pytest tests/ --cov=. --cov-report=xml
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
