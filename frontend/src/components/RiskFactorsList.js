import React from 'react';
import { AlertTriangle, TrendingUp, Info } from 'lucide-react';

const RiskFactorsList = ({ riskFactors }) => {
  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'high risk':
        return <AlertTriangle className="h-5 w-5 text-red-500" />;
      case 'medium risk':
        return <TrendingUp className="h-5 w-5 text-yellow-500" />;
      default:
        return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'high risk':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'medium risk':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      default:
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  const getFeatureLabel = (feature) => {
    const labels = {
      'age': 'Age',
      'education': 'Education Level',
      'sex': 'Sex',
      'is_smoking': 'Smoking Status',
      'cigsPerDay': 'Cigarettes per Day',
      'BPMeds': 'Blood Pressure Medication',
      'prevalentStroke': 'Previous Stroke',
      'prevalentHyp': 'Hypertension',
      'diabetes': 'Diabetes',
      'totChol': 'Total Cholesterol',
      'sysBP': 'Systolic Blood Pressure',
      'diaBP': 'Diastolic Blood Pressure',
      'BMI': 'Body Mass Index',
      'heartRate': 'Heart Rate',
      'glucose': 'Glucose Level'
    };
    return labels[feature] || feature;
  };


  return (
    <div>
      <h4 className="text-lg font-semibold text-red-800 mb-4 flex items-center">
        <AlertTriangle className="h-5 w-5 mr-2" />
        Risk Factors Identified
      </h4>
      
      <div className="grid md:grid-cols-2 gap-4">
        {riskFactors.map((factor, index) => (
          <div 
            key={index}
            className={`p-4 rounded-lg border-2 ${getStatusColor(factor.status)}`}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center">
                {getStatusIcon(factor.status)}
                <span className="font-semibold ml-2">
                  {getFeatureLabel(factor.feature)}
                </span>
              </div>
              <span className="text-sm font-medium">
                {factor.status}
              </span>
            </div>
            
            <div className="space-y-1">
              <div className="text-sm">
                <span className="font-medium">Current Value: </span>
                <span className="font-bold">{factor.value}</span>
              </div>
              
              <div className="text-sm">
                <span className="font-medium">Normal Range: </span>
                <span>{factor.normal_max}</span>
              </div>
              
              {factor.message && (
                <div className="text-sm mt-2 p-2 bg-white bg-opacity-50 rounded">
                  <span className="font-medium">Note: </span>
                  <span>{factor.message}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {riskFactors.length > 0 && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start">
            <Info className="h-5 w-5 text-red-600 mr-2 mt-0.5" />
            <div className="text-sm text-red-800">
              <strong>Important:</strong> These risk factors increase your likelihood of developing 
              Coronary Heart Disease. Please consult with your healthcare provider for personalized 
              advice and monitoring.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskFactorsList;