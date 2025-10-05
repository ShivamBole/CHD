import React from 'react';
import { 
  TrendingUp, 
  Shield, 
  AlertTriangle, 
  CheckCircle,
  Activity,
  Heart,
  Droplets,
  Scale,
  Zap,
  Target
} from 'lucide-react';

const RiskProgressionAnalysis = ({ riskProgression }) => {
  if (!riskProgression || riskProgression.length === 0) {
    return null;
  }

  const getFeatureIcon = (feature) => {
    switch (feature.toLowerCase()) {
      case 'totchol':
        return <Droplets className="h-5 w-5 text-blue-600" />;
      case 'sysbp':
      case 'diabp':
        return <Heart className="h-5 w-5 text-red-600" />;
      case 'bmi':
        return <Scale className="h-5 w-5 text-green-600" />;
      case 'heartrate':
        return <Activity className="h-5 w-5 text-purple-600" />;
      case 'glucose':
        return <Zap className="h-5 w-5 text-orange-600" />;
      default:
        return <Target className="h-5 w-5 text-gray-600" />;
    }
  };

  const getVulnerabilityColor = (vulnerability) => {
    switch (vulnerability) {
      case 'high':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'low':
        return 'bg-green-50 border-green-200 text-green-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getVulnerabilityIcon = (vulnerability) => {
    switch (vulnerability) {
      case 'high':
        return <AlertTriangle className="h-4 w-4 text-red-600" />;
      case 'medium':
        return <TrendingUp className="h-4 w-4 text-yellow-600" />;
      case 'low':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      default:
        return <Shield className="h-4 w-4 text-gray-600" />;
    }
  };

  return (
    <div className="medical-card rounded-xl p-6">
      <div className="flex items-center mb-6">
        <Shield className="h-6 w-6 text-blue-600 mr-2" />
        <h3 className="text-2xl font-semibold">Risk Progression Prevention Analysis</h3>
      </div>
      
      <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <TrendingUp className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
          <div className="text-sm text-blue-800">
            <strong>Prevention Focus:</strong> This analysis shows how much each health metric could 
            increase before becoming concerning, helping you understand which areas need the most attention 
            to maintain your low risk status.
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {riskProgression.map((item, index) => (
          <div 
            key={index}
            className={`p-4 rounded-lg border-2 ${getVulnerabilityColor(item.vulnerability)}`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center">
                {getFeatureIcon(item.feature)}
                <div className="ml-2">
                  <h4 className="font-semibold text-lg capitalize">
                    {item.feature.replace(/([A-Z])/g, ' $1').trim()}
                  </h4>
                  <div className="text-sm opacity-75">
                    Current: {item.current_value.toFixed(1)} | Normal: {item.normal_range}
                  </div>
                </div>
              </div>
              <div className="flex items-center">
                {getVulnerabilityIcon(item.vulnerability)}
                <span className="ml-2 text-sm font-medium capitalize">
                  {item.vulnerability} Vulnerability
                </span>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div className="bg-white bg-opacity-30 p-3 rounded">
                <div className="text-sm font-medium mb-1">Risk Threshold</div>
                <div className="text-lg font-bold">{item.risk_threshold}</div>
                <div className="text-xs opacity-75">Concerning level</div>
              </div>
              <div className="bg-white bg-opacity-30 p-3 rounded">
                <div className="text-sm font-medium mb-1">Increase Buffer</div>
                <div className="text-lg font-bold">+{item.increase_to_risk.toFixed(1)}</div>
                <div className="text-xs opacity-75">({item.increase_percentage.toFixed(0)}% increase)</div>
              </div>
            </div>

            <div className="space-y-2">
              <h5 className="font-medium text-sm">Prevention Strategy:</h5>
              <div className="grid md:grid-cols-3 gap-3">
                <div className="bg-white bg-opacity-20 p-2 rounded text-xs">
                  <div className="font-medium text-green-700 mb-1">🍽️ Diet</div>
                  <div>{item.recommendation.diet}</div>
                </div>
                <div className="bg-white bg-opacity-20 p-2 rounded text-xs">
                  <div className="font-medium text-blue-700 mb-1">🏃 Lifestyle</div>
                  <div>{item.recommendation.lifestyle}</div>
                </div>
                <div className="bg-white bg-opacity-20 p-2 rounded text-xs">
                  <div className="font-medium text-purple-700 mb-1">📊 Monitoring</div>
                  <div>{item.recommendation.monitoring}</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <div className="flex items-start">
          <CheckCircle className="h-5 w-5 text-green-600 mr-2 mt-0.5" />
          <div className="text-sm text-green-800">
            <strong>Key Insight:</strong> By focusing on the metrics with higher vulnerability scores, 
            you can create a targeted prevention plan that maximizes your protection against future 
            cardiovascular risk increases.
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskProgressionAnalysis;




