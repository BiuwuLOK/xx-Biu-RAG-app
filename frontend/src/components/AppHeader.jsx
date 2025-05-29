import React from 'react';

const AppHeader = () => {
  return (
    <div className="mb-8 text-center">
      <h1 className="text-3xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-blue-500">
        BiuBiu RAG App
      </h1>
      <p className="text-lg text-gray-600">
        您的個人 GitHub 專案 AI 助手 - 更聰明地了解和探索您的代碼庫
      </p>
    </div>
  );
};

export default AppHeader;
