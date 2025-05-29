import React from 'react';

const LoadedReposDisplay = ({ repos, isLoaded }) => {
  if (!isLoaded) return null;
  
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-3">已載入的倉庫</h2>
      <div className="bg-gray-50 rounded-lg p-4">
        <ul className="list-disc list-inside">
          {repos.map((repo, index) => (
            <li key={index} className="text-gray-600">
              {repo.name}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LoadedReposDisplay;
