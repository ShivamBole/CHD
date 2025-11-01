import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const RiskChart = ({ results }) => {
  const { 
    probability_disease, 
    probability_no_disease, 
    risk_level, 
    confidence 
  } = results;

  // Define risk colors and handle all possible formats
  const getRiskColor = (riskLevel) => {
    if (!riskLevel) return '#10b981'; // Default to green
    
    const level = String(riskLevel).toUpperCase();
    if (level.includes('HIGH')) return '#ef4444'; // Red
    if (level.includes('MEDIUM')) return '#f59e0b'; // Orange
    if (level.includes('LOW')) return '#10b981'; // Green
    return '#10b981'; // Default to green
  };
  
  const riskColor = getRiskColor(risk_level);

  // Probability pie chart data
  const probabilityData = [
    { name: 'CHD Risk', value: probability_disease * 100, color: riskColor },
    { name: 'No CHD Risk', value: probability_no_disease * 100, color: '#3b82f6' }
  ];

  const COLORS = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'];

  return (
    <div className="space-y-8">
      {/* Probability Chart */}
      <div>
        <h4 className="text-lg font-semibold mb-4 text-center">Risk Probability Distribution</h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={probabilityData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
                fill="#8884d8"
              >
                {probabilityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)}%`, 'Probability']}
                labelStyle={{ color: '#374151' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex justify-center space-x-6 mt-4">
          {probabilityData.map((item, index) => (
            <div key={index} className="flex items-center">
              <div 
                className="w-4 h-4 rounded-full mr-2" 
                style={{ backgroundColor: item.color }}
              ></div>
              <span className="text-sm text-gray-600">{item.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Confidence Chart */}
      <div>
        <h4 className="text-lg font-semibold mb-4 text-center">Model Confidence</h4>
        <div className="h-32">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[{ name: 'Confidence', value: confidence * 100 }]} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)}%`, 'Confidence']}
                labelStyle={{ color: '#374151' }}
              />
              <Bar 
                dataKey="value" 
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Health Metrics Summary */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className={`p-4 rounded-lg ${
          String(risk_level).includes('HIGH') ? 'bg-red-50' : 
          String(risk_level).includes('MEDIUM') ? 'bg-orange-50' : 
          'bg-green-50'
        }`}>
          <h5 className={`font-semibold mb-2 ${
            String(risk_level).includes('HIGH') ? 'text-red-800' : 
            String(risk_level).includes('MEDIUM') ? 'text-orange-800' : 
            'text-green-800'
          }`}>Risk Level</h5>
          <div className={`text-2xl font-bold ${
            String(risk_level).includes('HIGH') ? 'text-red-600' : 
            String(risk_level).includes('MEDIUM') ? 'text-orange-600' : 
            'text-green-600'
          }`}>
            {results.risk_level}
          </div>
        </div>
        
        <div className="bg-blue-50 p-4 rounded-lg">
          <h5 className="font-semibold text-blue-800 mb-2">Confidence Score</h5>
          <div className="text-2xl font-bold text-blue-600">
            {(confidence * 100).toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskChart;