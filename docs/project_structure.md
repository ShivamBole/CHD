# 📁 CHD Prediction System - Project Structure

This document provides a detailed overview of the project structure and explains the purpose of each directory and file.

## 🏗️ Root Directory Structure

```
CHD_Prediction_System/
├── 📁 backend/                    # Flask API Backend
├── 📁 frontend/                   # React Frontend Application
├── 📁 docs/                       # Project Documentation
├── 📁 data/                       # Data Files and Models
├── 📁 scripts/                    # Automation Scripts
├── 📁 deployment/                 # Deployment Configurations
├── 📄 README.md                   # Main project documentation
├── 📄 .gitignore                  # Git ignore rules
├── 📄 docker-compose.yml          # Docker container orchestration
└── 📄 env.example                 # Environment variables template
```

## 🔧 Backend Structure (`/backend/`)

```
backend/
├── 📁 api/                        # API Layer
├── 📁 models/                     # ML Models & Data Processing
├── 📁 services/                   # Business Logic Layer
├── 📁 utils/                      # Utility Functions
├── 📁 data/                       # Model Files & Data
│   ├── model.pkl                 # Trained ML model
│   ├── scaler.pkl                # Feature scaler
│   └── feature_columns.pkl       # Feature column names
├── 📁 tests/                      # Backend Tests
├── 📄 chd_prediction_api.py       # Main Flask application
├── 📄 train_model.py              # Model training script
├── 📄 config.py                   # Configuration settings
└── 📄 requirements.txt            # Python dependencies
```

## 🎨 Frontend Structure (`/frontend/`)

```
frontend/
├── 📁 public/                     # Static Files
├── 📁 src/                        # Source Code
│   ├── 📁 components/            # React Components
│   │   ├── 📁 common/           # Reusable Components
│   │   ├── 📁 forms/            # Form Components
│   │   ├── 📁 results/          # Results Components
│   │   └── 📁 layout/           # Layout Components
│   ├── 📁 services/             # API Services
│   ├── 📁 hooks/                # Custom React Hooks
│   ├── 📁 utils/                # Utility Functions
│   └── 📁 styles/               # Styling
├── 📁 tests/                     # Frontend Tests
├── 📄 package.json               # Node.js dependencies
└── 📄 tailwind.config.js         # Tailwind CSS configuration
```

## 📚 Documentation Structure (`/docs/`)

```
docs/
├── 📁 api/                       # API Documentation
├── 📁 user-guide/               # User Documentation
├── 📁 development/              # Development Documentation
├── 📁 architecture/             # System Architecture
└── 📄 README.md                  # Main documentation
```

## 📊 Data Structure (`/data/`)

```
data/
├── 📁 raw/                       # Raw Data Files
├── 📁 processed/                 # Processed Data
└── 📁 models/                    # Saved Models
```

## 🚀 Scripts Structure (`/scripts/`)

```
scripts/
├── 📁 setup/                     # Setup Scripts
├── 📁 deployment/                # Deployment Scripts
├── 📄 start_dev.sh              # Development startup (Linux/Mac)
└── 📄 start_dev.bat             # Development startup (Windows)
```

## 🔄 Data Flow

```
User Input → Frontend → API Gateway → Backend Services → ML Model → Response
     ↓           ↓           ↓              ↓              ↓         ↓
  React App → Axios → Flask API → Prediction → Model.pkl → JSON
     ↓           ↓           ↓              ↓              ↓         ↓
  UI Update ← State ← Response ← Business Logic ← Scaler ← Results
```

## 📋 File Naming Conventions

### Backend Files
- **Python files**: `snake_case.py`
- **Configuration**: `config.py`, `settings.py`
- **Tests**: `test_*.py`
- **Models**: `*_model.py`

### Frontend Files
- **React components**: `PascalCase.jsx`
- **Hooks**: `use*.js`
- **Services**: `*Service.js`
- **Utilities**: `camelCase.js`

### Documentation
- **Markdown files**: `kebab-case.md`
- **Images**: `descriptive-name.png`

## 🎯 Best Practices

### Code Organization
1. **Separation of Concerns**: Keep business logic separate from presentation
2. **Modular Design**: Create reusable components and utilities
3. **Clear Naming**: Use descriptive names for files and functions
4. **Documentation**: Document all public APIs and complex logic

### File Structure
1. **Logical Grouping**: Group related files in directories
2. **Consistent Naming**: Follow established naming conventions
3. **Clear Hierarchy**: Maintain clear directory structure
4. **Version Control**: Use `.gitignore` appropriately

This structure ensures maintainability, scalability, and ease of development for the CHD Prediction System.