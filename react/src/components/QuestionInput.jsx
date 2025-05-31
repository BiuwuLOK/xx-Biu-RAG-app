import React from 'react';

const QuestionInput = ({ question, setQuestion, onAskAssistant, loading, isLoaded }) => {
  if (!isLoaded) return null;

  return (
    <div className="mb-6">
      <label htmlFor="question" className="block text-lg font-semibold text-gray-700 mb-2">
        向我的 GitHub 助手提問：
      </label>
      <textarea
        id="question"
        rows="4"
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200 resize-y"
        placeholder="例如：您在 XBiu-AI-Quant-System 專案中使用了哪些機器學習模型？或者，您在 fMRI 專案中如何處理數據？"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        disabled={loading}
      />
      <button
        onClick={onAskAssistant}
        className="mt-4 w-full px-6 py-3 bg-green-600 text-white font-bold rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        disabled={loading}
      >
        {loading && (
          <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        )}
        詢問 GitHub 助手
      </button>
    </div>
  );
};

export default QuestionInput;
