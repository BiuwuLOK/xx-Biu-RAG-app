import React from 'react';

const AppFooter = () => {
  return (
    <footer className="mt-8 text-center text-gray-500 text-sm">
      <p>
        © {new Date().getFullYear()} BiuBiu RAG App. 
        使用 React、FastAPI 和 OpenAI 開發。
      </p>
    </footer>
  );
};

export default AppFooter;
