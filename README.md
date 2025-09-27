# 🫀 CHD Prediction System

A comprehensive Coronary Heart Disease (CHD) prediction system with machine learning backend and modern React frontend. This professional-grade application provides personalized health assessments and risk analysis for cardiovascular disease prevention.

## 🏗️ Project Structure

```
CHD_Prediction_System/
├── 📁 backend/                    # Flask API Backend
│   ├── 📁 api/                   # API layer
│   ├── 📁 models/                # ML models & data processing
│   ├── 📁 services/              # Business logic
│   ├── 📁 utils/                 # Utilities
│   ├── 📁 data/                  # Model files & data
│   ├── 📁 tests/                 # Backend tests
│   ├── chd_prediction_api.py     # Main API server
│   ├── train_model.py            # Model training script
│   ├── start_system.py           # System startup
│   └── requirements.txt          # Python dependencies
│
├── 📁 frontend/                  # React Frontend
│   ├── 📁 src/                   # Source code
│   │   ├── 📁 components/        # React components
│   │   ├── 📁 services/          # API services
│   │   ├── 📁 hooks/             # Custom hooks
│   │   ├── 📁 utils/             # Utilities
│   │   └── 📁 styles/            # Styling
│   ├── 📁 public/                # Static files
│   ├── package.json              # Node dependencies
│   └── tailwind.config.js        # Tailwind configuration
│
├── 📁 docs/                      # Documentation
│   ├── 📁 api/                   # API documentation
│   ├── 📁 user-guide/            # User guides
│   ├── 📁 development/           # Development docs
│   └── 📁 architecture/          # System architecture
│
├── 📁 data/                      # Data files
│   ├── 📁 raw/                   # Raw datasets
│   ├── 📁 processed/             # Processed data
│   └── 📁 models/                # Saved models
│
├── 📁 scripts/                   # Automation scripts
│   ├── 📁 setup/                 # Setup scripts
│   └── 📁 deployment/            # Deployment scripts
│
└── 📁 deployment/                # Deployment configurations
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **npm** or **yarn**

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Train the model (first time only)
python train_model.py

# Start the API server
python chd_prediction_api.py
```

The API will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React app
npm start
```

The React app will be available at `http://localhost:3000`

### 3. Using the System

1. Open `http://localhost:3000` in your browser
2. Fill in the health assessment form
3. Submit to get your CHD risk prediction
4. Review personalized recommendations

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data processing
- **Matplotlib/Seaborn** - Visualizations

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client

## 📊 Features

### Health Assessment
- **15+ Health Metrics** analysis
- **Real-time Risk Prediction** using ML
- **Interactive Visualizations** with charts
- **Personalized Recommendations**

### Risk Analysis
- **Feature Importance** ranking
- **Risk Factor** identification
- **Normal vs Abnormal** value comparison
- **Visual Risk Dashboard**

### Professional UI
- **Medical-grade Design** optimized for healthcare
- **Responsive Layout** for all devices
- **Accessible Interface** following best practices
- **Clean, Modern Aesthetics**

## 🔧 Development

### API Endpoints

- `GET /health` - API health check
- `POST /predict` - Get CHD risk prediction
- `POST /analyze` - Detailed risk analysis

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://localhost:3000
```

### Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

## 📈 Model Performance

The Random Forest classifier achieves:
- **Accuracy**: >85%
- **Precision**: >80%
- **Recall**: >75%
- **F1-Score**: >77%

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment

1. **Backend**: Deploy Flask app to your preferred hosting service
2. **Frontend**: Build React app and deploy to static hosting
3. **Update API URL** in frontend configuration

## 📋 Health Metrics

The system analyzes these health parameters:

### Demographics
- Age, Education Level, Sex

### Lifestyle Factors
- Smoking Status, Cigarettes per Day

### Medical History
- Blood Pressure Medication, Previous Stroke
- Hypertension, Diabetes

### Current Health
- Total Cholesterol, Blood Pressure (Systolic/Diastolic)
- BMI, Heart Rate, Glucose Level

## 🔒 Security & Privacy

- **No Data Storage** - Patient data is not persisted
- **Stateless API** - All requests are independent
- **HIPAA-compliant** design patterns
- **CORS Protection** configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

1. **API not responding**: Check if backend is running on port 5000
2. **CORS errors**: Verify CORS configuration in Flask app
3. **Model not found**: Run `python train_model.py` first
4. **Frontend build errors**: Check Node.js version and dependencies

### Getting Help

- Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- Review [API Documentation](docs/api/)
- Open an issue on GitHub

## 🎯 Future Enhancements

- [ ] User authentication and profiles
- [ ] Historical data tracking
- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Advanced ML models
- [ ] Mobile app version
- [ ] Integration with health devices

---

**⚠️ Medical Disclaimer**: This system is for educational and research purposes only. It should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.