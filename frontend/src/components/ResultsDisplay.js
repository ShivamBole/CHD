import React from 'react';
import { 
  Heart, 
  AlertTriangle, 
  CheckCircle, 
  TrendingUp, 
  Activity,
  ArrowLeft,
  BarChart3,
  Shield,
  Target
} from 'lucide-react';
import RiskChart from './RiskChart';
import RiskFactorsList from './RiskFactorsList';
import RecommendationsList from './RecommendationsList';
import RiskFactorsChart from './RiskFactorsChart';

const ResultsDisplay = ({ results, onReset }) => {
  const { 
    prediction, 
    risk_level, 
    probability_no_disease, 
    probability_disease, 
    confidence, 
    model_name,
    risk_factors,
    recommendations,
    normal_ranges,
    actual_values
  } = results;
  
  const getRiskColor = (level) => {
    if (!level) return 'risk-low';
    
    const levelStr = String(level).toLowerCase();
    if (levelStr.includes('high')) return 'risk-high';
    if (levelStr.includes('medium') || levelStr.includes('moderate')) return 'risk-medium';
    if (levelStr.includes('low')) return 'risk-low';
    return 'risk-low';
  };

  const getRiskIcon = (level) => {
    if (!level) return <CheckCircle className="h-6 w-6" />;
    
    const levelStr = String(level).toLowerCase();
    if (levelStr.includes('high')) return <AlertTriangle className="h-6 w-6" />;
    if (levelStr.includes('medium')) return <TrendingUp className="h-6 w-6" />;
    if (levelStr.includes('low')) return <CheckCircle className="h-6 w-6" />;
    return <CheckCircle className="h-6 w-6" />;
  };
  
  // Calculate risk analysis summary data
  const riskAnalysis = {
    total_risk_factors: risk_factors ? risk_factors.length : 0,
    total_normal_values: normal_ranges ? Object.keys(normal_ranges).length - (risk_factors ? risk_factors.length : 0) : 0,
    risk_factors: risk_factors || [],
    normal_values: []
  };
  
  // Prepare normal values array for display
  if (normal_ranges && actual_values) {
    Object.entries(normal_ranges).forEach(([feature, range]) => {
      const value = actual_values[feature];
      const isRiskFactor = risk_factors && risk_factors.some(factor => factor.feature === feature);
      
      if (!isRiskFactor && value !== undefined) {
        riskAnalysis.normal_values.push({
          feature,
          value,
          normal_range: range
        });
      }
    });
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <button
          onClick={onReset}
          className="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          New Assessment
        </button>
      </div>

      {/* Risk Summary Card */}
      <div className={`medical-card rounded-2xl p-8 border-2 ${getRiskColor(risk_level)}`}>
        <div className="text-center">
          <div className="flex justify-center items-center mb-4">
            {getRiskIcon(risk_level)}
          </div>
          <h2 className="text-3xl font-bold mb-2">Risk Assessment Complete</h2>
          <div className={`inline-block px-6 py-3 rounded-full text-lg font-semibold ${getRiskColor(risk_level)}`}>
            {risk_level}
          </div>
        </div>
      </div>

      {/* Probability Cards */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="medical-card rounded-xl p-6">
          <div className="flex items-center mb-4">
            <Heart className="h-6 w-6 text-red-600 mr-2" />
            <h3 className="text-xl font-semibold">CHD Risk Probability</h3>
          </div>
          <div className="text-4xl font-bold text-red-600 mb-2">
            {(probability_disease * 100).toFixed(1)}%
          </div>
          <p className="text-gray-600">
            Risk of developing Coronary Heart Disease in the next 10 years
          </p>
        </div>

        <div className="medical-card rounded-xl p-6">
          <div className="flex items-center mb-4">
            <Shield className="h-6 w-6 text-green-600 mr-2" />
            <h3 className="text-xl font-semibold">No CHD Risk</h3>
          </div>
          <div className="text-4xl font-bold text-green-600 mb-2">
            {(probability_no_disease * 100).toFixed(1)}%
          </div>
          <p className="text-gray-600">
            Probability of remaining free from CHD
          </p>
        </div>
      </div>

      {/* Risk Analysis */}
      <div className="medical-card rounded-xl p-6">
        <div className="flex items-center mb-6">
          <BarChart3 className="h-6 w-6 text-blue-600 mr-2" />
          <h3 className="text-2xl font-semibold">Risk Analysis Summary</h3>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6 mb-6">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {riskAnalysis.total_risk_factors}
            </div>
            <div className="text-sm text-gray-600">Risk Factors Found</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {riskAnalysis.total_normal_values}
            </div>
            <div className="text-sm text-gray-600">Normal Values</div>
          </div>
          
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {recommendations ? recommendations.length : 0}
            </div>
            <div className="text-sm text-gray-600">Recommendations</div>
          </div>
        </div>

        {/* Risk Factors Chart */}
        {risk_factors && risk_factors.length > 0 && normal_ranges && actual_values && (
          <RiskFactorsChart 
            riskFactors={risk_factors} 
            normalRanges={normal_ranges} 
            actualValues={actual_values} 
          />
        )}

        {/* Risk Factors */}
        {riskAnalysis.risk_factors && riskAnalysis.risk_factors.length > 0 && (
          <RiskFactorsList riskFactors={riskAnalysis.risk_factors} />
        )}

        {/* Normal Values */}
        {riskAnalysis.normal_values && riskAnalysis.normal_values.length > 0 && (
          <div className="mt-6">
            <h4 className="text-lg font-semibold text-green-800 mb-4 flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              Normal Health Values
            </h4>
            <div className="grid md:grid-cols-2 gap-4">
              {riskAnalysis.normal_values.slice(0, 6).map((item, index) => (
                <div key={index} className="bg-green-50 p-3 rounded-lg">
                  <div className="font-medium text-green-800">{item.feature}</div>
                  <div className="text-sm text-green-600">
                    {item.value} {typeof item.normal_range === 'object' && item.normal_range.unit? 
                      `(${item.normal_range.min}-${item.normal_range.max} ${item.normal_range.unit || ''})` : 
                      `${item.normal_range.unit ?( item.normal_range):""}`
                      }
                      
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Visualizations */}
      <div className="medical-card rounded-xl p-6">
        <div className="flex items-center mb-6">
          <Activity className="h-6 w-6 text-purple-600 mr-2" />
          <h3 className="text-2xl font-semibold">Risk Probability Visualization</h3>
        </div>
        <RiskChart results={results} />
      </div>

      {/* Health Recommendations */}
      <div className="medical-card rounded-xl p-6">
        <div className="flex items-center mb-6">
          <Heart className="h-6 w-6 text-red-600 mr-2" />
          <h3 className="text-2xl font-semibold">Health Recommendations</h3>
        </div>
        
        {recommendations && recommendations.length > 0 ? (
          <RecommendationsList recommendations={recommendations} />
        ) : (
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">General Health Tips</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Maintain a healthy diet rich in fruits, vegetables, and whole grains</li>
                <li>• Exercise regularly (at least 150 minutes of moderate activity per week)</li>
                <li>• Avoid smoking and limit alcohol consumption</li>
                <li>• Monitor your blood pressure and cholesterol levels regularly</li>
                <li>• Maintain a healthy weight and BMI</li>
              </ul>
            </div>
            
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h4 className="font-semibold text-green-800 mb-2">Next Steps</h4>
              <ul className="text-sm text-green-700 space-y-1">
                <li>• Schedule regular check-ups with your healthcare provider</li>
                <li>• Discuss these results with your doctor for personalized advice</li>
                <li>• Consider lifestyle modifications based on your risk factors</li>
                <li>• Monitor your health metrics regularly</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="text-center space-x-4">
        <button
          onClick={onReset}
          className="medical-button"
        >
          <Target className="h-5 w-5 inline mr-2" />
          New Assessment
        </button>
        
        <button
          onClick={() => window.print()}
          className="px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-colors"
        >
          Print Results
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;