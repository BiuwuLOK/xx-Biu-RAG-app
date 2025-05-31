import React from 'react';
import MessageBox from './MessageBox';

const AssistantAnswerDisplay = ({ answer, isLoaded }) => {
  if (!isLoaded || !answer) return null;
  
  return (
    <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg shadow-inner">
      <h2 className="text-xl font-bold text-blue-800 mb-3">助手回答：</h2>
      <MessageBox message={answer} type="assistant" />
    </div>
  );
};

export default AssistantAnswerDisplay;
