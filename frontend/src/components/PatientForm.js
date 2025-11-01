import React, { useState } from 'react';
import { User, Heart, Activity, AlertCircle, Loader2 } from 'lucide-react';

const PatientForm = ({ onSubmit, loading, error }) => {
  const [formData, setFormData] = useState({
    age: '',
    education: '2',
    sex: 'Male',
    is_smoking: 'No',
    cigsPerDay: '0',
    BPMeds: 'No',
    prevalentStroke: 'No',
    prevalentHyp: 'No',
    diabetes: 'No',
    totChol: '',
    sysBP: '',
    diaBP: '',
    BMI: '',
    heartRate: '',
    glucose: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const educationOptions = [
    { value: '1', label: 'Less than High School' },
    { value: '2', label: 'High School' },
    { value: '3', label: 'Some College' },
    { value: '4', label: 'College Graduate' }
  ];

  return (
    <div>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Patient Health Assessment
        </h2>
        <p className="text-gray-600">
          Please provide accurate health information for the best risk assessment
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
            <span className="text-red-700">{error}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Demographics Section */}
        <div className="bg-gray-50 p-6 rounded-xl">
          <div className="flex items-center mb-4">
            <User className="h-5 w-5 text-blue-600 mr-2" />
            <h3 className="text-xl font-semibold text-gray-900">Demographics</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age *
              </label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                className="medical-input"
                placeholder="Enter age (18-100)"
                min="18"
                max="100"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Education Level *
              </label>
              <select
                name="education"
                value={formData.education}
                onChange={handleChange}
                className="medical-input"
                required
              >
                {educationOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sex *
              </label>
              <select
                name="sex"
                value={formData.sex}
                onChange={handleChange}
                className="medical-input"
                required
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>
        </div>

        {/* Lifestyle Section */}
        <div className="bg-gray-50 p-6 rounded-xl">
          <div className="flex items-center mb-4">
            <Activity className="h-5 w-5 text-green-600 mr-2" />
            <h3 className="text-xl font-semibold text-gray-900">Lifestyle & Habits</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Smoking Status *
              </label>
              <select
                name="is_smoking"
                value={formData.is_smoking}
                onChange={handleChange}
                className="medical-input"
                required
              >
                <option value="No">Non-smoker</option>
                <option value="Yes">Smoker</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cigarettes per Day
              </label>
              <input
                type="number"
                name="cigsPerDay"
                value={formData.cigsPerDay}
                onChange={handleChange}
                className="medical-input"
                placeholder="0 if non-smoker"
                min="0"
                max="50"
              />
            </div>
          </div>
        </div>

        {/* Medical History Section */}
        <div className="bg-gray-50 p-6 rounded-xl">
          <div className="flex items-center mb-4">
            <Heart className="h-5 w-5 text-red-600 mr-2" />
            <h3 className="text-xl font-semibold text-gray-900">Medical History</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Blood Pressure Medication
              </label>
              <select
                name="BPMeds"
                value={formData.BPMeds}
                onChange={handleChange}
                className="medical-input"
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Previous Stroke
              </label>
              <select
                name="prevalentStroke"
                value={formData.prevalentStroke}
                onChange={handleChange}
                className="medical-input"
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hypertension
              </label>
              <select
                name="prevalentHyp"
                value={formData.prevalentHyp}
                onChange={handleChange}
                className="medical-input"
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diabetes
              </label>
              <select
                name="diabetes"
                value={formData.diabetes}
                onChange={handleChange}
                className="medical-input"
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </div>
          </div>
        </div>

        {/* Current Health Metrics */}
        <div className="bg-gray-50 p-6 rounded-xl">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Current Health Metrics
          </h3>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Total Cholesterol (mg/dL) *
              </label>
              <input
                type="number"
                name="totChol"
                value={formData.totChol}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 200"
                min="100"
                max="500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Systolic BP (mmHg) *
              </label>
              <input
                type="number"
                name="sysBP"
                value={formData.sysBP}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 120"
                min="80"
                max="250"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diastolic BP (mmHg) *
              </label>
              <input
                type="number"
                name="diaBP"
                value={formData.diaBP}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 80"
                min="40"
                max="150"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                BMI (kg/m²) *
              </label>
              <input
                type="number"
                name="BMI"
                value={formData.BMI}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 25.0"
                min="15"
                max="60"
                step="0.1"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Heart Rate (bpm) *
              </label>
              <input
                type="number"
                name="heartRate"
                value={formData.heartRate}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 75"
                min="40"
                max="200"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Glucose (mg/dL) *
              </label>
              <input
                type="number"
                name="glucose"
                value={formData.glucose}
                onChange={handleChange}
                className="medical-input"
                placeholder="e.g., 85"
                min="50"
                max="400"
                required
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center">
          <button
            type="submit"
            disabled={loading}
            className="medical-button text-lg px-8 py-4"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin inline mr-2" />
                Analyzing Health Data...
              </>
            ) : (
              <>
                <Heart className="h-5 w-5 inline mr-2" />
                Get Risk Assessment
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientForm;