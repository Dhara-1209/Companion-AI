# 🏠 HomeBuddy - AI-Powered Smart Home Assistant

<div align="center">

![HomeBuddy](https://img.shields.io/badge/HomeBuddy-Smart%20Home%20Assistant-blue?style=for-the-badge&logo=home)

**Your Intelligent Companion for Home Appliance Management & Maintenance**

[![React](https://img.shields.io/badge/React-18.3-blue?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live Demo](#-quick-start) • [Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation)

</div>

---

## 🎯 What is HomeBuddy?

HomeBuddy is an **AI-powered smart home management system** that revolutionizes how you maintain and troubleshoot your household appliances. From instant error code diagnosis to predictive maintenance scheduling, HomeBuddy helps you save time, money, and avoid unnecessary service calls.

### 💡 Key Problems We Solve

- **🔧 Instant Troubleshooting**: Natural language AI assistant that understands your appliance issues
- **💸 Cost Savings**: Avoid $150-300 service calls with AI-guided DIY repairs
- **📊 Predictive Maintenance**: Smart alerts before problems occur
- **🛡️ Safety First**: Built-in safety protocols with emergency detection
- **📚 Comprehensive Coverage**: 15+ brands, 40+ error codes, 500+ manual pages

---

## ✨ Features

### 🤖 AI-Powered Diagnosis
- Natural language processing for appliance troubleshooting
- RAG (Retrieval-Augmented Generation) technology with 652 manual chunks
- Real-time chat interface with step-by-step repair guidance
- Response time under 3 seconds

### 📱 Appliance Management
- Track all your home appliances in one place
- Store device information (brand, model, serial number, warranty)
- Monitor appliance health and lifecycle
- Device status dashboard

### 🔧 Repair History Tracking
- Log all repair incidents and maintenance activities
- Track repair costs and service dates
- Identify recurring issues with pattern analysis
- Generate comprehensive repair statistics

### ⏰ Predictive Maintenance
- 6-month automated reminder system
- Schedule regular maintenance tasks (e.g., lint filter cleaning)
- Warranty expiration tracking
- Smart maintenance notifications

### 🛡️ Safety-First Architecture
- 4-level safety system: Safe → Caution → Danger → Emergency
- Automatic detection of hazards (gas leaks, electrical issues)
- Professional referral recommendations when needed
- Transparent cost estimates for repairs

### 📊 Comprehensive Database
- **5 Appliance Categories**: Washing Machines, Dishwashers, Ovens, Microwaves, Vacuum Cleaners
- **15+ Brands**: Samsung, LG, Bosch, Whirlpool, GE, Maytag, and more
- **40+ Error Codes**: Detailed explanations and solutions
- **500+ Manual Pages**: Fully indexed and searchable

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Hetvi2211/Homebuddy.git
cd Homebuddy

# Install frontend dependencies
npm install --legacy-peer-deps

# Install backend dependencies
pip install -r requirements.txt
```

### Running the Application

**Frontend:**
```bash
npm run dev
# Access at: http://localhost:5173
```

**Backend:**
```bash
python src/backend/main.py
# API runs on: http://localhost:8000
```

**Quick Demo (Windows):**
```bash
./start_companion_ai.bat
```

---

## 🛠️ Tech Stack

### Frontend
- **React 18.3.1** - Modern UI library
- **TypeScript 5+** - Type-safe development
- **Vite 6.3.5** - Lightning-fast build tool
- **Tailwind CSS v4** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Material-UI** - Rich component library

### Backend
- **FastAPI** - High-performance Python API framework
- **Uvicorn** - ASGI server
- **Python 3.11** - Backend logic

### AI & Data
- **Vector Search** - Semantic document retrieval
- **RAG Pipeline** - Retrieval-Augmented Generation
- **Natural Language Processing** - Query understanding

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 📂 Project Structure

```
Homebuddy/
├── src/
│   ├── app/
│   │   ├── components/        # React components
│   │   ├── pages/            # Application pages
│   │   └── styles/           # CSS and styling
│   ├── backend/
│   │   └── main.py           # FastAPI server
│   ├── config/               # Configuration files
│   └── tests/                # Test suites
├── data/                     # Appliance manuals and data
├── docker/                   # Docker configuration
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── docker-compose.yml        # Docker orchestration
├── package.json              # Node dependencies
├── requirements.txt          # Python dependencies
└── vite.config.ts           # Vite configuration
```

---

## 🎬 Demo Scenarios

### 1. 💧 Drainage Issue
**User**: "My washing machine won't drain water"  
**HomeBuddy**: Instant 5-step solution with safety checks

### 2. ⚠️ Error Code Diagnosis
**User**: "E3 error on Samsung WF42H5200"  
**HomeBuddy**: Brand-specific troubleshooting guide

### 3. 🚨 Safety Alert
**User**: "Gas smell from oven"  
**HomeBuddy**: Emergency protocol activation + professional referral

### 4. 🔧 Quick Fix
**User**: "Microwave turntable not spinning"  
**HomeBuddy**: 2-minute DIY repair instructions

---

## 👥 Team

Built with ❤️ by 4 dedicated developers:

- **[Hetvi2211](https://github.com/Hetvi2211)** - Project Lead & Frontend Architecture
- **[Krrishna-2210](https://github.com/Krrishna-2210)** - Backend Development & API Design
- **[unnatii14](https://github.com/unnatii14)** - Feature Implementation & Business Logic
- **[Dhara-1209](https://github.com/Dhara-1209)** - QA, Testing & Documentation

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📊 Performance Metrics

- ⚡ **Response Time**: < 3 seconds
- 🎯 **Accuracy Rate**: 85%
- 😊 **User Satisfaction**: 78%
- 📚 **Manual Coverage**: 500+ pages indexed
- 🔍 **Error Code Database**: 40+ codes supported

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Built for hackathon innovation
- Powered by modern AI and RAG technology
- Inspired by the need to make home maintenance accessible to everyone

---

<div align="center">

**Made with 💙 by the HomeBuddy Team**

[⭐ Star us on GitHub](https://github.com/Hetvi2211/Homebuddy) • [🐛 Report Bug](https://github.com/Hetvi2211/Homebuddy/issues) • [✨ Request Feature](https://github.com/Hetvi2211/Homebuddy/issues)

</div>
