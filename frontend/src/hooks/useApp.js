import { useGitHubReposLoader } from './useGitHubReposLoader';
import { useAssistant } from './useAssistant';

export const useApp = () => {
  const {
    githubUsername,
    setGithubUsername,
    loading: githubLoading,
    reposData,
    isLoaded,
    message,
    messageType,
    showMessage,
    clearMessage,
    loadGitHubRepos,
  } = useGitHubReposLoader();

  const {
    question,
    setQuestion,
    answer,
    loading: assistantLoading,
    askAssistant,
  } = useAssistant(githubUsername, showMessage);

  const loading = githubLoading || assistantLoading;

  return {
    // GitHub 相關
    githubUsername,
    setGithubUsername,
    reposData,
    isLoaded,
    loadGitHubRepos,
    
    // 消息相關
    message,
    messageType,
    showMessage,
    clearMessage,
    
    // 問答相關
    question,
    setQuestion,
    answer,
    askAssistant,
    
    // 載入狀態
    loading,
  };
};
