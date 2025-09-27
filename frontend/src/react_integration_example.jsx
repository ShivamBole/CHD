import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CHDPredictionApp = () => {
  const [formData, setFormData] = useState({
    age: '',
    education: '1',
    sex: 'M',
    is_smoking: 'NO',
    cigsPerDay: '0',
    BPMeds: 'NO',
    prevalentStroke: 'NO',
    prevalentHyp: 'NO',
    diabetes: 'NO',
    totChol: '',
    sysBP: '',
    diaBP: '',
    BMI: '',
    heartRate: '',
    glucose: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/predict', formData);
      setPrediction(response.data);
    } catch (err) {
      setError('Error making prediction. Please try again.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const RiskIndicator = ({ riskLevel, probability }) => {
    const riskColor = riskLevel === 'High Risk' ? '#ff6b6b' : '#51cf66';
    const riskIcon = riskLevel === 'High Risk' ? '⚠️' : '✅';
    
    return (
      <div className="risk-indicator" style={{ 
        backgroundColor: riskColor, 
        color: 'white', 
        padding: '20px', 
        borderRadius: '10px',
        textAlign: 'center',
        margin: '20px 0'
      }}>
        <h2>{riskIcon} {riskLevel}</h2>
        <p>CHD Probability: {(probability.chd * 100).toFixed(1)}%</p>
        <p>No CHD Probability: {(probability.no_chd * 100).toFixed(1)}%</p>
      </div>
    );
  };

  const RiskFactorsList = ({ riskFactors }) => {
    if (!riskFactors || riskFactors.length === 0) {
      return (
        <div className="no-risk-factors">
          <h3>✅ No Risk Factors Detected</h3>
          <p>All your health metrics are within normal ranges!</p>
        </div>
      );
    }

    return (
      <div className="risk-factors">
        <h3>⚠️ Risk Factors Detected ({riskFactors.length})</h3>
        {riskFactors.map((factor, index) => (
          <div key={index} className="risk-factor-item" style={{
            backgroundColor: '#fff3cd',
            border: '1px solid #ffeaa7',
            padding: '15px',
            margin: '10px 0',
            borderRadius: '5px'
          }}>
            <h4>{factor.feature}</h4>
            <p><strong>Your Value:</strong> {factor.value}</p>
            <p><strong>Normal Range:</strong> {factor.normal_range}</p>
            <p><strong>Status:</strong> {factor.status}</p>
            <p><strong>Message:</strong> {factor.message}</p>
          </div>
        ))}
      </div>
    );
  };

  const RecommendationsList = ({ recommendations }) => {
    if (!recommendations || recommendations.length === 0) return null;

    return (
      <div className="recommendations">
        <h3>💡 Health Recommendations</h3>
        {recommendations.map((rec, index) => (
          <div key={index} className={`recommendation ${rec.type}`} style={{
            backgroundColor: rec.type === 'urgent' ? '#ffebee' : 
                           rec.type === 'warning' ? '#fff3e0' : '#e8f5e8',
            border: `1px solid ${rec.type === 'urgent' ? '#f44336' : 
                               rec.type === 'warning' ? '#ff9800' : '#4caf50'}`,
            padding: '15px',
            margin: '10px 0',
            borderRadius: '5px'
          }}>
            <h4>{rec.title}</h4>
            <p>{rec.message}</p>
          </div>
        ))}
      </div>
    );
  };

  const VisualizationDisplay = ({ visualization }) => {
    if (!visualization) return null;

    return (
      <div className="visualization">
        <h3>📊 Risk Analysis Dashboard</h3>
        <img 
          src={`data:image/png;base64,${visualization}`} 
          alt="Risk Analysis Dashboard"
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </div>
    );
  };

  return (
    <div className="chd-prediction-app" style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1>🫀 CHD Risk Prediction System</h1>
      <p>Enter your health information to get a personalized CHD risk assessment.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Input Form */}
        <div className="input-form">
          <h2>Health Information</h2>
          <form onSubmit={handleSubmit}>
            {/* Demographics */}
            <div className="form-section">
              <h3>Demographics</h3>
              <div className="form-group">
                <label>Age:</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  required
                  min="18"
                  max="100"
                />
              </div>
              
              <div className="form-group">
                <label>Sex:</label>
                <select name="sex" value={formData.sex} onChange={handleInputChange}>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>

              <div className="form-group">
                <label>Education Level:</label>
                <select name="education" value={formData.education} onChange={handleInputChange}>
                  <option value="1">Higher Secondary</option>
                  <option value="2">Graduation</option>
                  <option value="3">Post Graduation</option>
                  <option value="4">PhD</option>
                </select>
              </div>
            </div>

            {/* Lifestyle */}
            <div className="form-section">
              <h3>Lifestyle</h3>
              <div className="form-group">
                <label>Smoking Status:</label>
                <select name="is_smoking" value={formData.is_smoking} onChange={handleInputChange}>
                  <option value="NO">No</option>
                  <option value="YES">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>Cigarettes per Day:</label>
                <input
                  type="number"
                  name="cigsPerDay"
                  value={formData.cigsPerDay}
                  onChange={handleInputChange}
                  min="0"
                  max="50"
                />
              </div>
            </div>

            {/* Medical History */}
            <div className="form-section">
              <h3>Medical History</h3>
              <div className="form-group">
                <label>Blood Pressure Medication:</label>
                <select name="BPMeds" value={formData.BPMeds} onChange={handleInputChange}>
                  <option value="NO">No</option>
                  <option value="YES">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>Previous Stroke:</label>
                <select name="prevalentStroke" value={formData.prevalentStroke} onChange={handleInputChange}>
                  <option value="NO">No</option>
                  <option value="YES">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>Hypertension:</label>
                <select name="prevalentHyp" value={formData.prevalentHyp} onChange={handleInputChange}>
                  <option value="NO">No</option>
                  <option value="YES">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>Diabetes:</label>
                <select name="diabetes" value={formData.diabetes} onChange={handleInputChange}>
                  <option value="NO">No</option>
                  <option value="YES">Yes</option>
                </select>
              </div>
            </div>

            {/* Current Health Metrics */}
            <div className="form-section">
              <h3>Current Health Metrics</h3>
              <div className="form-group">
                <label>Total Cholesterol (mg/dL):</label>
                <input
                  type="number"
                  name="totChol"
                  value={formData.totChol}
                  onChange={handleInputChange}
                  min="100"
                  max="400"
                />
              </div>

              <div className="form-group">
                <label>Systolic BP (mmHg):</label>
                <input
                  type="number"
                  name="sysBP"
                  value={formData.sysBP}
                  onChange={handleInputChange}
                  min="80"
                  max="200"
                />
              </div>

              <div className="form-group">
                <label>Diastolic BP (mmHg):</label>
                <input
                  type="number"
                  name="diaBP"
                  value={formData.diaBP}
                  onChange={handleInputChange}
                  min="40"
                  max="120"
                />
              </div>

              <div className="form-group">
                <label>BMI (kg/m²):</label>
                <input
                  type="number"
                  name="BMI"
                  value={formData.BMI}
                  onChange={handleInputChange}
                  min="15"
                  max="50"
                  step="0.1"
                />
              </div>

              <div className="form-group">
                <label>Heart Rate (bpm):</label>
                <input
                  type="number"
                  name="heartRate"
                  value={formData.heartRate}
                  onChange={handleInputChange}
                  min="40"
                  max="200"
                />
              </div>

              <div className="form-group">
                <label>Glucose (mg/dL):</label>
                <input
                  type="number"
                  name="glucose"
                  value={formData.glucose}
                  onChange={handleInputChange}
                  min="50"
                  max="300"
                />
              </div>
            </div>

            <button type="submit" disabled={loading} style={{
              backgroundColor: '#007bff',
              color: 'white',
              padding: '15px 30px',
              border: 'none',
              borderRadius: '5px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              width: '100%'
            }}>
              {loading ? 'Analyzing...' : 'Get Risk Assessment'}
            </button>
          </form>
        </div>

        {/* Results Display */}
        <div className="results-display">
          <h2>Risk Assessment Results</h2>
          
          {error && (
            <div style={{ color: 'red', padding: '10px', backgroundColor: '#ffebee', borderRadius: '5px' }}>
              {error}
            </div>
          )}

          {prediction && (
            <div>
              <RiskIndicator 
                riskLevel={prediction.risk_level} 
                probability={prediction.probability} 
              />
              
              <RiskFactorsList riskFactors={prediction.risk_analysis.risk_factors} />
              
              <RecommendationsList recommendations={prediction.recommendations} />
              
              <VisualizationDisplay visualization={prediction.visualization} />
            </div>
          )}

          {!prediction && !loading && (
            <div style={{ 
              textAlign: 'center', 
              padding: '40px', 
              color: '#666',
              backgroundColor: '#f8f9fa',
              borderRadius: '10px'
            }}>
              <h3>Ready for Assessment</h3>
              <p>Fill in your health information and click "Get Risk Assessment" to see your personalized CHD risk analysis.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CHDPredictionApp;