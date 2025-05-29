import React from 'react';

const GitHubReposLoader = ({ username, setUsername, onLoadRepos, loading }) => {
  return (
    <div className="mb-6">
      <label htmlFor="githubUsername" className="block text-lg font-semibold text-gray-700 mb-2">
        您的 GitHub 用戶名 (預設為我的):
      </label>
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          id="githubUsername"
          className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
          placeholder="例如：BiuwuLOK"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
        />
        <button
          onClick={onLoadRepos}
          className="px-6 py-3 bg-indigo-600 text-white font-bold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          disabled={loading}
        >
          {loading && (
            <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          )}
          載入 GitHub 倉庫
        </button>
      </div>
    </div>
  );
};

export default GitHubReposLoader;
