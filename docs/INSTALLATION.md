# 🔧 CompanionAI Installation & Setup Guide

## 📋 Prerequisites

Before installing CompanionAI, ensure you have the following:

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free disk space
- **Internet**: Required for initial setup and model downloads

### Required Software
- **Python 3.8+**: [Download from python.org](https://www.python.org/downloads/)
- **Git**: [Download from git-scm.com](https://git-scm.com/downloads/)
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/companion-ai.git
   cd companion-ai
   ```

2. **Run Setup Script**
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   **macOS/Linux:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the Application**
   ```bash
   ./start_companion_ai.bat  # Windows
   ./start_companion_ai.sh   # macOS/Linux
   ```

### Option 2: Manual Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/companion-ai.git
   cd companion-ai
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment
   .venv\Scripts\activate     # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the System**
   ```bash
   python scripts/initialize.py
   ```

## 🔧 Detailed Setup Instructions

### Step 1: Environment Setup

#### Windows Setup
1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install Git**
   - Download from [git-scm.com](https://git-scm.com/downloads/)
   - Use default installation options
   - Verify: `git --version`

#### macOS Setup
1. **Install Python 3.8+**
   ```bash
   # Using Homebrew (recommended)
   brew install python@3.9
   
   # Or download from python.org
   ```

2. **Install Git**
   ```bash
   # Using Homebrew
   brew install git
   
   # Or use Xcode Command Line Tools
   xcode-select --install
   ```

#### Linux Setup (Ubuntu/Debian)
1. **Install Python 3.8+**
   ```bash
   sudo apt update
   sudo apt install python3.9 python3.9-venv python3-pip
   ```

2. **Install Git**
   ```bash
   sudo apt install git
   ```

### Step 2: Project Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/companion-ai.git
   cd companion-ai
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate it
   # Windows:
   .venv\Scripts\activate
   
   # macOS/Linux:
   source .venv/bin/activate
   
   # Verify activation (should show (.venv) in prompt)
   which python  # Should point to .venv/bin/python
   ```

3. **Upgrade pip**
   ```bash
   python -m pip install --upgrade pip
   ```

### Step 3: Dependencies Installation

1. **Install Core Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import streamlit, fastapi; print('Dependencies installed successfully!')"
   ```

### Step 4: System Initialization

1. **Initialize Vector Database**
   ```bash
   python scripts/initialize.py
   ```
   
   This will:
   - Process appliance manuals
   - Create vector embeddings
   - Build FAISS index
   - Set up error code database

2. **Verify Setup**
   ```bash
   python scripts/verify_setup.py
   ```

## ▶️ Running the Application

### Method 1: Using Start Scripts

**Windows:**
```cmd
start_companion_ai.bat
```

**macOS/Linux:**
```bash
./start_companion_ai.sh
```

### Method 2: Manual Startup

1. **Start Backend Server**
   ```bash
   # Terminal 1
   python -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start Frontend Application**
   ```bash
   # Terminal 2 (new terminal)
   streamlit run src/frontend/app.py --server.port 8501
   ```

3. **Access Application**
   - Open browser to: `http://localhost:8501`
   - API docs available at: `http://localhost:8000/docs`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Frontend Configuration
FRONTEND_PORT=8501

# AI Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_SEARCH_RESULTS=5
RELEVANCE_THRESHOLD=0.7

# Safety Configuration
SAFETY_CHECK_ENABLED=true
EMERGENCY_ALERT_THRESHOLD=0.9

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/companion_ai.log
```

### Custom Configuration

Edit `config/settings.yaml`:

```yaml
# CompanionAI Configuration
app:
  name: "CompanionAI"
  version: "1.0.0"
  debug: false

api:
  host: "127.0.0.1"
  port: 8000
  cors_origins: ["http://localhost:8501"]

frontend:
  port: 8501
  theme: "purple"
  max_file_size: "100MB"

ai:
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  max_tokens: 4000
  temperature: 0.1
  top_k: 5

safety:
  enabled: true
  strict_mode: true
  emergency_threshold: 0.9
```

## 🐳 Docker Installation (Alternative)

### Using Docker Compose

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/companion-ai.git
   cd companion-ai
   ```

2. **Build and Run**
   ```bash
   docker-compose up --build
   ```

3. **Access Application**
   - Frontend: `http://localhost:8501`
   - Backend: `http://localhost:8000`

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
```

## 🔍 Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "Port already in use"
**Solution:**
```bash
# Find process using port
netstat -tulpn | grep :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

#### Issue: "FAISS index not found"
**Solution:**
```bash
# Reinitialize the system
python scripts/initialize.py --force
```

#### Issue: "Backend connection failed"
**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check firewall settings
3. Restart backend server
4. Check logs: `tail -f logs/api_metrics.log`

### Performance Issues

#### Slow Response Times
1. **Reduce vector search results:**
   ```python
   # In config/settings.yaml
   ai:
     top_k: 3  # Reduce from 5
   ```

2. **Optimize memory usage:**
   ```bash
   # Set environment variable
   export OMP_NUM_THREADS=2
   ```

#### High Memory Usage
1. **Monitor memory:**
   ```bash
   # Linux/macOS
   top -p $(pgrep -f uvicorn)
   
   # Windows
   tasklist /fi "imagename eq python.exe"
   ```

2. **Reduce batch size:**
   ```python
   # In src/core/models/companion_ai.py
   BATCH_SIZE = 16  # Reduce if needed
   ```

### Debugging Mode

Enable detailed logging:

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or edit .env file
echo "LOG_LEVEL=DEBUG" >> .env

# Restart application
```

## 📊 Verification & Testing

### Health Checks

1. **Backend Health**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend Access**
   ```bash
   curl http://localhost:8501
   ```

3. **AI Engine Test**
   ```bash
   python scripts/test_ai_engine.py
   ```

### Performance Tests

```bash
# Run comprehensive tests
python scripts/run_tests.py

# Specific component tests
python -m pytest tests/test_backend.py
python -m pytest tests/test_frontend.py
python -m pytest tests/test_ai_engine.py
```

### Load Testing

```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f tests/load_test.py --host http://localhost:8000
```

## 🔄 Updates & Maintenance

### Updating CompanionAI

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

2. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Migrate Data**
   ```bash
   python scripts/migrate_data.py
   ```

4. **Restart Services**
   ```bash
   ./restart_services.sh
   ```

### Backup & Restore

**Backup:**
```bash
python scripts/backup.py --output backup_$(date +%Y%m%d).tar.gz
```

**Restore:**
```bash
python scripts/restore.py --input backup_20250919.tar.gz
```

## 📈 Monitoring & Logs

### Log Files
- **Application Logs**: `logs/companion_ai.log`
- **API Metrics**: `logs/api_metrics.log`
- **Error Logs**: `logs/errors.log`
- **Access Logs**: `logs/access.log`

### Monitoring Commands

```bash
# Monitor application logs
tail -f logs/companion_ai.log

# Monitor API performance
tail -f logs/api_metrics.log | grep "processing_time"

# Check error rates
grep "ERROR" logs/errors.log | tail -20

# Monitor resource usage
htop  # Linux/macOS
tasklist  # Windows
```

## 🆘 Support

### Getting Help

1. **Check Documentation**: Review all `.md` files in `/docs`
2. **Search Issues**: Look for similar problems in GitHub issues
3. **Run Diagnostics**: Use `python scripts/diagnose.py`
4. **Contact Support**: Create an issue with diagnostic output

### Community Resources

- **GitHub Issues**: [Report bugs and request features](https://github.com/your-username/companion-ai/issues)
- **Discussions**: [Join community discussions](https://github.com/your-username/companion-ai/discussions)
- **Wiki**: [Community knowledge base](https://github.com/your-username/companion-ai/wiki)

---

**Next Steps**: After successful installation, see [USER-GUIDE.md](./USER-GUIDE.md) to learn how to use CompanionAI effectively.