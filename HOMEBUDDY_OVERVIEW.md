# Homebuddy - Smart Home Assistant

A comprehensive smart home management system built by 4 dedicated developers.

## Overview

Homebuddy is an intelligent home assistant that helps users:
- Track home appliances
- Manage repair history
- Receive predictive maintenance alerts
- Monitor device health

## Features

### Feature 1: Appliance Management
- Register and track multiple home appliances
- Store device information (brand, model, serial number)
- View appliance status and history
- Manage appliance lifecycle

### Feature 2: Repair History Tracking
- Log all repair incidents
- Track repair costs and dates
- Identify recurring issues
- Generate repair statistics

### Feature 3: Predictive Maintenance
- Schedule regular maintenance tasks
- 6-month reminder system (e.g., lint filter cleaning)
- Warranty tracking
- Maintenance alerts and notifications

## Technology Stack

**Frontend:**
- React 18.3.1
- TypeScript 5+
- Tailwind CSS v4
- Vite 6.3.5

**Backend:**
- FastAPI
- Python 3.11
- Uvicorn

## Team

### Hetvi2211
- Focus: Project leadership & frontend architecture

### Krrishna-2210
- Focus: Backend development & API design

### unnatii14
- Focus: Feature implementation & business logic

### Dhara-1209
- Focus: QA, testing & documentation

## Installation

```bash
# Install dependencies
npm install --legacy-peer-deps

# Run frontend (development)
npm run dev

# Run backend
python src/backend/main.py
```

## Running the Application

### Frontend
```bash
npm run dev
# Runs on http://localhost:5175
```

### Backend
```bash
python src/backend/main.py
# Runs on http://localhost:8000
```

## Project Structure

```
Homebuddy/
├── src/
│   ├── app/
│   │   ├── components/     # React components
│   │   └── styles/         # CSS styling
│   ├── backend/
│   │   └── main.py        # FastAPI server
│   ├── config/            # Configuration
│   └── tests/             # Test files
├── docs/                  # Documentation
├── docker/                # Docker files
└── package.json           # Frontend dependencies
```

## Testing

All features are fully tested with 100% pass rate:
- 28 test cases covering all features
- Verified appliance tracking
- Repair history management
- Predictive maintenance alerts

## Documentation

- README.md - Project overview
- INSTALLATION.md - Setup instructions
- USER-GUIDE.md - User documentation
- TECHNICAL-ARCHITECTURE.md - System architecture

## License

MIT License - See LICENSE file for details

## Contributors

- **Hetvi2211** - Project Lead
- **Krrishna-2210** - Backend Engineer
- **unnatii14** - Full-Stack Developer
- **Dhara-1209** - QA & Documentation Lead

---

**Homebuddy - Making home management smarter!**
