import React from 'react';
import { Heart, Activity } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">CHD Prediction</h1>
              <p className="text-sm text-gray-600">Coronary Heart Disease Risk Assessment</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Activity className="h-4 w-4" />
            <span>Powered by Machine Learning</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;