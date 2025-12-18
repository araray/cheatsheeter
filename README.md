# CheatSheeter 📝

A modern, themeable web application for creating and managing programming cheatsheets. Built with Flask (Python) backend and vanilla JavaScript frontend using jQuery and Bootstrap 5.

![CheatSheeter](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **📚 Create & Manage Cheatsheets**: Intuitive interface for creating programming reference guides
- **🎨 5 Beautiful Themes**: Default, Dark, Ocean, Forest, and Sunset themes with smooth transitions
- **🔍 Search & Filter**: Quickly find cheatsheets with real-time search
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **🔒 Security First**: Input validation, rate limiting, and protection against common vulnerabilities
- **🐳 Docker Ready**: Easy deployment with Docker and Docker Compose
- **💾 File-Based Storage**: YAML files for human-readable data storage
- **⚡ Fast & Lightweight**: Vanilla JavaScript with jQuery - no heavy frameworks

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized deployment)

### Installation

#### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/araray/cheatsheeter.git
cd cheatsheeter

# Start the application
docker-compose up -d

# Access the application
open http://localhost:5000
```

#### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/araray/cheatsheeter.git
cd cheatsheeter

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the backend
python app.py

# Access the application
open http://localhost:5000
```

## 📖 Usage

### Creating a Cheatsheet

1. Click "Create New" in the navigation bar
2. Enter a unique name (e.g., `python-basics`, `git-commands`)
3. Set the title and number of columns
4. Add categories with commands and descriptions
5. Click "Save Cheatsheet"

### Using the CLI

```bash
# Create a new cheatsheet
python cli.py create python-basics

# List all cheatsheets
python cli.py list

# Show cheatsheet details
python cli.py show python-basics

# Validate cheatsheet structure
python cli.py validate python-basics

# Delete a cheatsheet
python cli.py delete python-basics
```

## 🎨 Theming

CheatSheeter includes 5 built-in themes:

- **Default**: Clean, light theme (perfect for daytime)
- **Dark**: Easy on the eyes for night coding sessions
- **Ocean**: Deep blues and teals inspired by the sea
- **Forest**: Earthy greens for a natural feel
- **Sunset**: Warm oranges and purples for cozy vibes

Themes are automatically saved and persist across sessions using `localStorage`.

## 🏗️ Architecture

```
cheatsheeter-fixed/
├── backend/
│   ├── app.py              # Flask application with REST API
│   ├── models.py           # CheatSheet model with validation
│   ├── config.py           # Configuration management
│   ├── cli.py              # Command-line interface
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── cheatsheets/        # YAML storage (auto-created)
│
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main HTML page
│   ├── static/
│   │   ├── js/
│   │   │   ├── api.js      # API communication module
│   │   │   ├── theme.js    # Theme management
│   │   │   └── app.js      # Main application logic
│   │   ├── css/
│   │   │   └── main.css    # Custom styles
│   │   └── themes/
│   │       ├── default.css
│   │       ├── dark.css
│   │       ├── ocean.css
│   │       ├── forest.css
│   │       └── sunset.css
│
└── docker-compose.yml      # Container orchestration
```

## 🔒 Security Features

- **Input Validation**: Marshmallow schemas for data validation
- **Path Traversal Protection**: Secure filename handling with `werkzeug`
- **Rate Limiting**: Flask-Limiter prevents API abuse
- **XSS Protection**: HTML escaping on all user inputs
- **Atomic File Operations**: Prevents data corruption during writes
- **CORS Configuration**: Configurable allowed origins
- **Safe YAML Loading**: Uses `yaml.safe_load()` to prevent code execution

## 🐛 Bug Fixes from Original

This version fixes critical issues from the original codebase:

### Backend Fixes ✅

- **Fixed route typo** in `app.py` (`<n>` → `<name>`)
- **Added input validation** with Marshmallow schemas
- **Implemented atomic file writes** to prevent corruption
- **Added comprehensive error handling**
- **Implemented rate limiting**
- **Added security measures** (path traversal protection, XSS prevention)
- **Improved error responses** with proper HTTP status codes

### Frontend Fixes ✅

- **Removed duplicate catch blocks** in error handling
- **Added loading states** for better UX
- **Implemented proper error messages**
- **Added search/filter functionality**
- **Fixed localStorage handling** with fallbacks
- **Improved responsive design**
- **Added keyboard navigation support**

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/cheatsheets` | List all cheatsheets |
| GET | `/api/cheatsheets/<name>` | Get specific cheatsheet |
| POST | `/api/cheatsheets` | Create new cheatsheet |
| PUT | `/api/cheatsheets/<name>` | Update cheatsheet |
| DELETE | `/api/cheatsheets/<name>` | Delete cheatsheet |

See [API.md](./API.md) for detailed documentation.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Run all tests
./run_tests.sh
```

## 🚀 Deployment

### Production with Docker

```bash
# Set environment variables
export SECRET_KEY=$(openssl rand -hex 32)

# Build and run
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f backend
```

### Production without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## 🔧 Configuration

Environment variables:

```bash
FLASK_ENV=production          # Environment (development/production)
SECRET_KEY=your-secret-key    # Secret key for sessions
CHEATSHEETS_FOLDER=/path      # Storage directory
FLASK_HOST=0.0.0.0           # Host to bind to
FLASK_PORT=5000              # Port to listen on
ALLOWED_ORIGINS=http://...   # CORS allowed origins (comma-separated)
```

## 📝 Sample Cheatsheet YAML

```yaml
title: Python Basics
columns: 2
categories:
  - name: Variables
    column: 1
    items:
      - command: "x = 10"
        description: "Assign integer value"
      - command: "name = 'John'"
        description: "Assign string value"
  
  - name: Functions
    column: 2
    items:
      - command: "def greet():"
        description: "Define a function"
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- UI powered by [Bootstrap 5](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
- jQuery for DOM manipulation

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/araray/cheatsheeter/issues)
