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

const ResultsDisplay = ({ results, onReset }) => {
  const { risk_level, probability, risk_analysis, recommendations, visualization } = results;
  
  const getRiskColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high risk':
        return 'risk-high';
      case 'medium risk':
        return 'risk-medium';
      case 'low risk':
        return 'risk-low';
      default:
        return 'risk-low';
    }
  };

  const getRiskIcon = (level) => {
    switch (level.toLowerCase()) {
      case 'high risk':
        return <AlertTriangle className="h-6 w-6" />;
      case 'medium risk':
        return <TrendingUp className="h-6 w-6" />;
      case 'low risk':
        return <CheckCircle className="h-6 w-6" />;
      default:
        return <CheckCircle className="h-6 w-6" />;
    }
  };

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
            {(probability.chd * 100).toFixed(1)}%
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
            {(probability.no_chd * 100).toFixed(1)}%
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
              {risk_analysis.total_risk_factors}
            </div>
            <div className="text-sm text-gray-600">Risk Factors Found</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {risk_analysis.total_normal_values}
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

        {/* Risk Factors */}
        {risk_analysis.risk_factors && risk_analysis.risk_factors.length > 0 && (
          <RiskFactorsList riskFactors={risk_analysis.risk_factors} />
        )}

        {/* Normal Values */}
        {risk_analysis.normal_values && risk_analysis.normal_values.length > 0 && (
          <div className="mt-6">
            <h4 className="text-lg font-semibold text-green-800 mb-4 flex items-center">
              <CheckCircle className="h-5 w-5 mr-2" />
              Normal Health Values
            </h4>
            <div className="grid md:grid-cols-2 gap-4">
              {risk_analysis.normal_values.slice(0, 6).map((item, index) => (
                <div key={index} className="bg-green-50 p-3 rounded-lg">
                  <div className="font-medium text-green-800">{item.feature}</div>
                  <div className="text-sm text-green-600">
                    {item.value} ({item.normal_range})
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Visualizations */}
      {visualization && (
        <div className="medical-card rounded-xl p-6">
          <div className="flex items-center mb-6">
            <Activity className="h-6 w-6 text-purple-600 mr-2" />
            <h3 className="text-2xl font-semibold">Health Analysis Charts</h3>
          </div>
          <RiskChart results={results} />
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <RecommendationsList recommendations={recommendations} />
      )}

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