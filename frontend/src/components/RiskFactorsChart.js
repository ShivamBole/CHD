import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const RiskFactorsChart = ({ riskFactors, normalRanges, actualValues }) => {
  if (!riskFactors || riskFactors.length === 0) {
    return null;
  }

  // Prepare data for the chart
  const chartData = riskFactors.map(factor => {
    const feature = factor.feature;
    const value = actualValues[feature];
    const range = normalRanges[feature];
    
    let normalValue = 0;
    if (range && typeof range === 'object') {
      normalValue = range.max || 0;
    }
    
    return {
      name: getFeatureLabel(feature),
      value: value,
      normalValue: normalValue
    };
  });

  // Helper function to get readable labels
  function getFeatureLabel(feature) {
    const labels = {
      'age': 'Age',
      'education': 'Education',
      'sex': 'Sex',
      'is_smoking': 'Smoking',
      'cigsPerDay': 'Cigarettes/Day',
      'BPMeds': 'BP Medication',
      'prevalentStroke': 'Stroke',
      'prevalentHyp': 'Hypertension',
      'diabetes': 'Diabetes',
      'totChol': 'Cholesterol',
      'sysBP': 'Systolic BP',
      'diaBP': 'Diastolic BP',
      'BMI': 'BMI',
      'heartRate': 'Heart Rate',
      'glucose': 'Glucose'
    };
    return labels[feature] || feature;
  }

  return (
    <div className="mb-6">
      <h4 className="text-lg font-semibold mb-4 text-center">Risk Factors Comparison</h4>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#ef4444" name="Your Value" />
            <Bar dataKey="normalValue" fill="#10b981" name="Normal Max" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RiskFactorsChart;