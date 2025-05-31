import React from 'react';

const MessageBox = ({ message, type = 'user' }) => {
  const isAssistant = type === 'assistant';
  
  return (
    <div
      className={`p-4 rounded-lg mb-4 ${
        isAssistant 
          ? 'bg-blue-100 ml-4' 
          : 'bg-gray-100 mr-4'
      }`}
    >
      <div className="flex items-start">
        <div
          className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isAssistant ? 'bg-blue-500' : 'bg-gray-500'
          } text-white font-bold mr-3`}
        >
          {isAssistant ? 'A' : 'U'}
        </div>
        <div className="flex-1">
          <pre className="whitespace-pre-wrap font-sans">
            {message}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default MessageBox;
