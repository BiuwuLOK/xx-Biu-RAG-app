import { useState } from 'react';
import { BACKEND_URL } from '../config/constants';

export const useGitHubReposLoader = () => {
  const [githubUsername, setGithubUsername] = useState('BiuwuLOK');
  const [loading, setLoading] = useState(false);
  const [reposData, setReposData] = useState([]); // 更改 projectsData 为 reposData
  const [isLoaded, setIsLoaded] = useState(false); // 更改 isDataLoaded 为 isLoaded
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('info');

  const showMessage = (msg, type = 'info') => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => setMessage(''), 5000);
  };

  const clearMessage = () => {
    setMessage('');
  };

  const loadGitHubRepos = async () => { // 更改 loadGitHubProjects 为 loadGitHubRepos
    if (!githubUsername) {
      showMessage('請輸入 GitHub 用戶名！', 'error');
      return;
    }

    setLoading(true);
    setReposData([]);
    setIsLoaded(false);
    showMessage('正在載入 GitHub 倉庫數據，這可能需要一些時間...');

    try {
      const response = await fetch(`${BACKEND_URL}/load_github_projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: githubUsername }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `無法載入 GitHub 倉庫：${response.statusText}`);
      }

      const result = await response.json();
      setReposData([{ name: `已載入 ${result.projects_count} 個倉庫` }]);
      setIsLoaded(true);
      showMessage(result.message, 'info');

    } catch (error) {
      console.error('載入 GitHub 倉庫數據時發生錯誤:', error);
      showMessage(`載入 GitHub 倉庫數據失敗：${error.message}。請檢查用戶名或後端服務。`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return {
    githubUsername,
    setGithubUsername,
    loading,
    reposData,          // 更新返回值
    isLoaded,           // 更新返回值
    message,
    messageType,
    showMessage,
    clearMessage,
    loadGitHubRepos,    // 更新返回值
  };
};
