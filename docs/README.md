# 🫀 CHD Prediction React App

A modern React application for predicting Coronary Heart Disease (CHD) risk using machine learning. This app integrates with a Flask API to provide personalized health assessments and recommendations.

## 🚀 Features

- **Comprehensive Health Assessment**: 15+ health metrics analysis
- **Real-time Risk Prediction**: ML-powered 10-year CHD risk assessment
- **Interactive Visualizations**: Charts and graphs for health data
- **Personalized Recommendations**: Tailored health advice based on risk factors
- **Professional Medical UI**: Clean, responsive design optimized for healthcare
- **Risk Factor Analysis**: Detailed breakdown of abnormal health values

## 🛠️ Tech Stack

- **Frontend**: React 18, Tailwind CSS, Recharts
- **Backend**: Flask API (Python)
- **ML**: Scikit-learn, Random Forest Classifier
- **Icons**: Lucide React
- **Styling**: Tailwind CSS with custom medical theme

## 📦 Installation

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+ (for the API)
- npm or yarn

### Setup Instructions

1. **Install React Dependencies**
   ```bash
   npm install
   ```

2. **Start the Flask API** (in a separate terminal)
   ```bash
   python chd_prediction_api.py
   ```

3. **Start the React App**
   ```bash
   npm start
   ```

4. **Open in Browser**
   Navigate to `http://localhost:3000`

## 🏥 Health Metrics Analyzed

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

## 📊 API Integration

The app connects to the Flask API at `http://localhost:5000`:

- **POST /predict**: Get CHD risk prediction
- **GET /health**: Check API status
- **POST /analyze**: Detailed risk analysis

## 🎨 UI Components

- **PatientForm**: Comprehensive health data input
- **ResultsDisplay**: Risk assessment results with visualizations
- **RiskChart**: Interactive charts using Recharts
- **RiskFactorsList**: Detailed risk factor analysis
- **RecommendationsList**: Personalized health advice

## 🔧 Development

### Project Structure
```
src/
├── components/
│   ├── Header.js
│   ├── PatientForm.js
│   ├── ResultsDisplay.js
│   ├── RiskChart.js
│   ├── RiskFactorsList.js
│   └── RecommendationsList.js
├── App.js
├── index.js
└── index.css
```

### Customization

- **Styling**: Modify `tailwind.config.js` for theme changes
- **API Endpoint**: Update API URL in `App.js`
- **Health Metrics**: Add/remove fields in `PatientForm.js`

## 📱 Responsive Design

- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interface
- Accessible design patterns

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Netlify**: Drag and drop the `build` folder
- **Vercel**: Connect your GitHub repository
- **AWS S3**: Upload build files to S3 bucket

## 🔒 Security & Privacy

- No data stored locally
- API calls are stateless
- Patient data not persisted
- HIPAA-compliant design patterns

## 📈 Performance

- Optimized bundle size
- Lazy loading for charts
- Efficient re-renders
- Fast API responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the API is running on port 5000
2. Verify all dependencies are installed
3. Check browser console for errors
4. Ensure CORS is enabled in the Flask API

## 🎯 Future Enhancements

- [ ] User authentication
- [ ] Historical data tracking
- [ ] Export to PDF
- [ ] Multi-language support
- [ ] Advanced visualizations
- [ ] Mobile app version