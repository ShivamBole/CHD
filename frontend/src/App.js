import React, { useState } from 'react';
import PatientForm from './components/PatientForm';
import ResultsDisplay from './components/ResultsDisplay';
import Header from './components/Header';
import { Heart, Activity, Shield } from 'lucide-react';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePrediction = async (patientData) => {
    setLoading(true);
    setError(null);
    
    // Add education field if missing (required by backend)
    const dataWithEducation = {
      ...patientData,
      education: patientData.education || 4 // Default value if not provided
    };
    
    try {
      // First check if API is available
      const healthResponse = await fetch('http://127.0.0.1:8000/health', {
        method: 'GET',
        timeout: 5000
      });
      
      if (!healthResponse.ok) {
        throw new Error('API server is not responding. Please make sure the FastAPI server is running on port 8000.');
      }

      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataWithEducation),
        mode: 'cors'
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`API Error: ${response.status} - ${errorData.error || 'Unknown error'}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        setError('Failed to connect to API server. Please ensure the FastAPI server is running on http://127.0.0.1:8000');
      } else {
        setError(err.message);
      }
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!results ? (
          <div className="max-w-4xl mx-auto">
            {/* Hero Section */}
            <div className="text-center mb-12">
              <div className="flex justify-center items-center mb-6">
                <div className="bg-blue-100 p-4 rounded-full">
                  <Heart className="h-12 w-12 text-blue-600" />
                </div>
              </div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                CHD Risk Assessment
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Predict your 10-year risk of Coronary Heart Disease using advanced machine learning
              </p>
              
              {/* Features */}
              <div className="grid md:grid-cols-3 gap-6 mb-12">
                <div className="bg-white p-6 rounded-xl shadow-lg">
                  <Activity className="h-8 w-8 text-green-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Advanced Analysis</h3>
                  <p className="text-gray-600">15+ health metrics analyzed using ML algorithms</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-lg">
                  <Shield className="h-8 w-8 text-blue-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Personalized Results</h3>
                  <p className="text-gray-600">Get specific risk factors and recommendations</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-lg">
                  <Heart className="h-8 w-8 text-red-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Health Insights</h3>
                  <p className="text-gray-600">Visual charts and detailed health analysis</p>
                </div>
              </div>
            </div>

            {/* Form Section */}
            <div className="medical-card rounded-2xl shadow-2xl p-8">
              <PatientForm 
                onSubmit={handlePrediction} 
                loading={loading}
                error={error}
              />
            </div>
          </div>
        ) : (
          <div className="max-w-6xl mx-auto">
            <ResultsDisplay 
              results={results} 
              onReset={resetForm}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;