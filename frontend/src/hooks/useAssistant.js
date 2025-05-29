import { useState } from 'react';
import { BACKEND_URL } from '../config/constants';

export const useAssistant = (githubUsername, showMessage) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const askAssistant = async () => {
    if (!question.trim()) {
      showMessage('請輸入您的問題！', 'error');
      return;
    }

    setLoading(true);
    setAnswer('');
    showMessage('正在思考中，請稍候...');

    try {
      const response = await fetch(`${BACKEND_URL}/ask_assistant`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, username: githubUsername }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `無法獲取回答：${response.statusText}`);
      }

      const result = await response.json();
      setAnswer(result.answer);
      showMessage('回答已生成！', 'info');

    } catch (error) {
      console.error('向助手提問時發生錯誤:', error);
      setAnswer(`提問過程中發生錯誤。關於更多訊息請直接訪問作者(${githubUsername})的代碼托管棧(Repository): https://github.com/${githubUsername}`);
      showMessage(`提問失敗：${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return {
    question,
    setQuestion,
    answer,
    loading,
    askAssistant,
  };
};
