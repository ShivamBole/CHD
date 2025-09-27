import React from 'react';
import { Heart, Activity, Shield, Target, CheckCircle, AlertCircle } from 'lucide-react';

const RecommendationsList = ({ recommendations }) => {
  const getRecommendationIcon = (title) => {
    const titleLower = title.toLowerCase();
    if (titleLower.includes('exercise') || titleLower.includes('activity')) {
      return <Activity className="h-5 w-5 text-green-600" />;
    } else if (titleLower.includes('diet') || titleLower.includes('nutrition')) {
      return <Heart className="h-5 w-5 text-red-600" />;
    } else if (titleLower.includes('checkup') || titleLower.includes('monitor')) {
      return <Shield className="h-5 w-5 text-blue-600" />;
    } else if (titleLower.includes('smoking') || titleLower.includes('quit')) {
      return <Target className="h-5 w-5 text-orange-600" />;
    } else {
      return <CheckCircle className="h-5 w-5 text-purple-600" />;
    }
  };

  const getPriorityColor = (priority, index) => {
    // Use explicit priority if available, otherwise fall back to index-based
    const actualPriority = priority || (index === 0 ? 'urgent' : index === 1 ? 'high' : index === 2 ? 'medium' : 'low');
    
    switch (actualPriority) {
      case 'urgent':
        return 'bg-red-100 border-red-300 text-red-900';
      case 'high':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'preventive':
        return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'maintenance':
        return 'bg-green-50 border-green-200 text-green-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getPriorityLabel = (priority, index) => {
    const actualPriority = priority || (index === 0 ? 'urgent' : index === 1 ? 'high' : index === 2 ? 'medium' : 'low');
    
    switch (actualPriority) {
      case 'urgent':
        return 'Urgent Action';
      case 'high':
        return 'High Priority';
      case 'medium':
        return 'Medium Priority';
      case 'preventive':
        return 'Prevention Focus';
      case 'maintenance':
        return 'Maintain Health';
      default:
        return 'Recommended';
    }
  };

  return (
    <div className="medical-card rounded-xl p-6">
      <div className="flex items-center mb-6">
        <Heart className="h-6 w-6 text-red-600 mr-2" />
        <h3 className="text-2xl font-semibold">Personalized Health Recommendations</h3>
      </div>
      
      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div 
            key={index}
            className={`p-4 rounded-lg border-2 ${getPriorityColor(rec.priority, index)}`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center">
                {getRecommendationIcon(rec.title)}
                <h4 className="font-semibold ml-2 text-lg">{rec.title}</h4>
              </div>
              <span className="text-sm font-medium px-2 py-1 rounded-full bg-white bg-opacity-50">
                {getPriorityLabel(rec.priority, index)}
              </span>
            </div>
            
            <p className="text-sm leading-relaxed mb-3">
              {rec.message}
            </p>
            
            {rec.details && (
              <div className="text-xs text-gray-600 bg-white bg-opacity-30 p-2 rounded">
                <strong>Additional Info:</strong> {rec.details}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* General Health Tips */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
          <div className="text-sm text-blue-800">
            <strong>Remember:</strong> These recommendations are based on your current health profile. 
            Always consult with your healthcare provider before making significant lifestyle changes, 
            especially if you have existing medical conditions.
          </div>
        </div>
      </div>
      
      {/* Action Items */}
      <div className="mt-6">
        <h4 className="font-semibold text-gray-800 mb-3">Next Steps:</h4>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="flex items-center p-3 bg-green-50 rounded-lg">
            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
            <span className="text-sm">Schedule a follow-up with your doctor</span>
          </div>
          <div className="flex items-center p-3 bg-green-50 rounded-lg">
            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
            <span className="text-sm">Start implementing the recommendations</span>
          </div>
          <div className="flex items-center p-3 bg-green-50 rounded-lg">
            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
            <span className="text-sm">Monitor your progress regularly</span>
          </div>
          <div className="flex items-center p-3 bg-green-50 rounded-lg">
            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
            <span className="text-sm">Reassess in 6-12 months</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsList;