# 📋 Project Structure & File Reference

## Complete File Listing

```
scihub.py/
│
├── 📄 Core Application Files
│   ├── app.py                    Flask backend application with REST API
│   ├── run.py                    Application entry point
│   ├── config.py                 Configuration settings
│   └── requirements.txt           Python dependencies
│
├── 📁 Frontend
│   └── templates/
│       └── index.html            Beautiful web interface (HTML/CSS/JS)
│
├── 📁 Core Library
│   ├── scihub/
│   │   └── scihub.py             Original SciHub Python library
│   └── README.md                 Original project README
│
├── 📁 Downloads Storage
│   └── downloads/                Auto-created folder for PDF storage
│
├── 🐳 Docker & Deployment
│   ├── Dockerfile                Docker image configuration
│   ├── docker-compose.yml        Docker Compose orchestration
│   ├── start.sh                  Bash startup script
│   └── verify.sh                 Installation verification script
│
├── 📚 Documentation
│   ├── QUICKSTART.md             Quick start guide (READ THIS FIRST!)
│   ├── WEB_APP_README.md         Complete web app documentation
│   ├── DEPLOYMENT.md             Production deployment guide
│   ├── FEATURES.md               Feature reference & capabilities
│   └── FILE_REFERENCE.md         This file
│
└── 📋 Repository Files
    ├── .git/                     Git version control
    ├── .gitignore                Git ignore rules
    └── LICENSE                   Project license
```

## File Descriptions

### 🔧 Core Application Files

#### `app.py` (Flask Backend)
**Purpose**: Main Flask application with REST API endpoints  
**Size**: ~12KB  
**Key Functions**:
- REST API endpoints for search, download, fetch, and file listing
- Error handling and logging
- File serving for downloads
- Integration with SciHub library

**Key Endpoints**:
- `POST /api/search` - Search academic papers
- `POST /api/download` - Download papers
- `POST /api/fetch` - Get paper metadata
- `GET /api/downloads` - List downloaded papers
- `GET /download/<filename>` - Download file

#### `run.py` (Application Entry Point)
**Purpose**: Simple launcher that starts the Flask web server  
**Size**: ~1KB  
**Usage**:
```bash
python run.py
```
**Displays**: Banner with app URL and instructions

#### `config.py` (Configuration)
**Purpose**: Centralized configuration management  
**Size**: ~1KB  
**Settings**:
- Flask debug mode
- Server host/port
- File upload settings
- Search result limits
- Logging configuration

#### `requirements.txt` (Dependencies)
**Purpose**: Lists all Python packages needed  
**Packages**:
- `flask` - Web framework
- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing
- `retrying` - Retry decorator
- `pysocks` - Proxy support

### 🎨 Frontend Files

#### `templates/index.html` (Web Interface)
**Purpose**: Complete web application UI  
**Size**: ~20KB  
**Features**:
- Search interface
- Download options (by identifier or URL)
- Downloads manager
- Responsive design
- Real-time feedback
- Modern animations

**Sections**:
1. Header with branding
2. Search card
3. Download card
4. Downloads history card

**Technologies**:
- HTML5 semantic markup
- CSS3 with gradients and animations
- Vanilla JavaScript (no dependencies)

### 📦 Core Library

#### `scihub/scihub.py` (SciHub Library)
**Purpose**: Original Python library for searching and downloading papers  
**Size**: ~11KB  
**Key Classes**:
- `SciHub` - Main class with search/download functionality
- `CaptchaNeedException` - Custom exception

**Main Methods**:
- `search(query, limit)` - Search Google Scholar
- `download(identifier, destination)` - Download paper
- `fetch(identifier)` - Get paper without saving

**Identifiers Supported**:
- DOI (Digital Object Identifier)
- PMID (PubMed ID)
- URL

### 📁 Storage

#### `downloads/` (Downloads Folder)
**Purpose**: Stores all downloaded PDF papers  
**Auto-created**: Yes, on first download  
**Naming**: `<md5_hash>-<paper_id>.pdf`  
**Access**: Via web interface or direct file system

### 🐳 Docker & Deployment

#### `Dockerfile`
**Purpose**: Build Docker image for containerized deployment  
**Size**: ~1KB  
**Features**:
- Based on `python:3.11-slim`
- Automated dependency installation
- Health check included
- Optimized for production

**Build Command**:
```bash
docker build -t scihub-web .
```

#### `docker-compose.yml`
**Purpose**: Define Docker service and orchestration  
**Size**: ~0.3KB  
**Configuration**:
- Service name: `scihub-web`
- Port mapping: 5000→5000
- Volume mounting for downloads
- Auto-restart policy

**Usage**:
```bash
docker-compose up
```

#### `start.sh` (Startup Script)
**Purpose**: Convenient application launcher  
**Size**: ~1KB  
**Does**:
1. Checks Python installation
2. Installs dependencies
3. Creates downloads folder
4. Starts the application
5. Shows status banner

**Usage**:
```bash
chmod +x start.sh
./start.sh
```

#### `verify.sh` (Verification Script)
**Purpose**: Verify installation and dependencies  
**Size**: ~2KB  
**Checks**:
- Python version
- Required packages
- File structure
- Directory existence
- Flask import
- Shows installation status

**Usage**:
```bash
chmod +x verify.sh
./verify.sh
```

### 📚 Documentation Files

#### `QUICKSTART.md` (Quick Start Guide)
**Purpose**: Fast introduction to the app  
**Contents**:
- Overview of new features
- Quick start in 3 steps
- File structure
- Feature highlights
- Comparison to CLI version

**Read This First**: ✅ Yes!

#### `WEB_APP_README.md` (Complete Documentation)
**Purpose**: Comprehensive user and developer guide  
**Contents**:
- Feature list
- Installation instructions
- Detailed usage guide
- API endpoint documentation
- Troubleshooting tips
- Legal notice

**Best For**: Understanding features and troubleshooting

#### `DEPLOYMENT.md` (Production Deployment)
**Purpose**: Production deployment guide  
**Contents**:
- Local development setup
- Docker deployment
- Cloud deployment (Heroku, AWS, GCP, DigitalOcean)
- Linux server setup
- Nginx + SSL configuration
- Monitoring and maintenance
- Performance optimization
- Security checklist

**Best For**: Production deployments

#### `FEATURES.md` (Feature Reference)
**Purpose**: Complete feature documentation  
**Contents**:
- Core features list
- Download options
- UI features
- API features
- Performance details
- Security features
- Browser compatibility
- System requirements
- Deployment options
- Comparison charts

**Best For**: Feature reference

### 📋 Repository Files

#### `.gitignore`
**Purpose**: Specify files to ignore in Git  
**Ignores**:
- `__pycache__/` and `.pyc` files
- Virtual environments
- IDE settings
- Logs
- Downloads folder
- Environment files
- OS files

#### `LICENSE`
**Purpose**: Project license terms  
**Type**: MIT License (or as specified)

#### `README.md` (Original)
**Purpose**: Original SciHub.py project documentation  
**Reference**: For the underlying library

### 🎯 Development Files

#### `.git/`
**Purpose**: Git version control repository  
**Contains**: Commit history and branches

---

## Quick Reference Table

| File | Type | Size | Purpose |
|------|------|------|---------|
| `app.py` | Python | ~12KB | Flask API backend |
| `run.py` | Python | ~1KB | Launcher script |
| `config.py` | Python | ~1KB | Configuration |
| `templates/index.html` | HTML/CSS/JS | ~20KB | Web UI |
| `scihub/scihub.py` | Python | ~11KB | SciHub library |
| `Dockerfile` | Docker | ~1KB | Container config |
| `docker-compose.yml` | YAML | ~0.3KB | Compose config |
| `start.sh` | Bash | ~1KB | Startup script |
| `verify.sh` | Bash | ~2KB | Verification |
| `QUICKSTART.md` | Markdown | ~3KB | Quick guide |
| `WEB_APP_README.md` | Markdown | ~8KB | User guide |
| `DEPLOYMENT.md` | Markdown | ~12KB | Deploy guide |
| `FEATURES.md` | Markdown | ~8KB | Features |

## File Modification Guide

### To Customize:

1. **Port Number**: Edit `config.py` → `PORT`
2. **Theme/Colors**: Edit `templates/index.html` → CSS section
3. **Search Limits**: Edit `config.py` → `MAX_SEARCH_RESULTS`
4. **Logging Level**: Edit `config.py` → `LOG_LEVEL`
5. **Download Folder**: Edit `config.py` → `UPLOAD_FOLDER`

### To Deploy:

1. **Docker**: Use `Dockerfile` and `docker-compose.yml`
2. **Heroku**: Use `Procfile` (create one with: `web: gunicorn app:app`)
3. **VPS**: Follow `DEPLOYMENT.md` → Linux Server Setup
4. **Cloud**: See `DEPLOYMENT.md` → Cloud Deployment sections

### To Extend:

1. **New API Endpoint**: Add route in `app.py`
2. **New UI Page**: Add HTML in `templates/`
3. **New Feature**: Add Python function in new module
4. **Database**: Implement in `app.py` (consider SQLAlchemy)

## Performance Tips

- **Faster Starts**: Remove debug logging from `config.py`
- **Better Downloads**: Use Gunicorn: `pip install gunicorn`
- **More Concurrent Users**: Increase Gunicorn workers: `-w 8`
- **Caching**: Add Flask-Caching in `app.py`

## Security Tips

- Set `DEBUG = False` in `config.py` for production
- Use HTTPS with Nginx reverse proxy
- Implement rate limiting
- Validate all user inputs
- Keep dependencies updated
- Use environment variables for secrets

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Status**: Production Ready

For questions or issues, refer to the appropriate documentation file!
