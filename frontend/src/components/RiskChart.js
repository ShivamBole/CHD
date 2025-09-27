import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const RiskChart = ({ results }) => {
  const { probability, risk_analysis } = results;

  // Probability pie chart data
  const probabilityData = [
    { name: 'CHD Risk', value: probability.chd * 100, color: '#ef4444' },
    { name: 'No CHD Risk', value: probability.no_chd * 100, color: '#10b981' }
  ];

  // Risk factors bar chart data
  const riskFactorsData = risk_analysis.risk_factors?.map(factor => ({
    name: factor.feature,
    value: parseFloat(factor.value),
    normalRange: factor.normal_range,
    status: factor.status
  })) || [];

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

      {/* Risk Factors Chart */}
      {riskFactorsData.length > 0 && (
        <div>
          <h4 className="text-lg font-semibold mb-4 text-center">Risk Factors Analysis</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskFactorsData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="name" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip 
                  formatter={(value, name, props) => [
                    `${value} (${props.payload.normalRange})`,
                    'Current Value'
                  ]}
                  labelStyle={{ color: '#374151' }}
                />
                <Bar 
                  dataKey="value" 
                  fill="#ef4444"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Health Metrics Summary */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h5 className="font-semibold text-blue-800 mb-2">Risk Level</h5>
          <div className="text-2xl font-bold text-blue-600">
            {results.risk_level}
          </div>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h5 className="font-semibold text-green-800 mb-2">Total Risk Factors</h5>
          <div className="text-2xl font-bold text-green-600">
            {risk_analysis.total_risk_factors}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskChart;