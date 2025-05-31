import React from 'react';
import {
  MessageBox,
  AppHeader,
  GitHubReposLoader,
  LoadedReposDisplay,
  QuestionInput,
  AssistantAnswerDisplay,
  AppFooter
} from './components';
import { useApp } from './hooks/hooks';

// UI 組件定義
const AppUI = ({
  // GitHub 相關
  githubUsername,
  setGithubUsername,
  reposData,
  isLoaded,
  loadGitHubRepos,
  
  // 消息相關
  message,
  messageType,
  clearMessage,
  
  // 問答相關
  question,
  setQuestion,
  answer,
  askAssistant,
  
  // 載入狀態
  loading,
}) => (
  <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 sm:p-6 lg:p-8 font-inter text-gray-800 flex flex-col items-center">
    <MessageBox message={message} type={messageType} onClose={clearMessage} />

    <div className="w-full max-w-4xl bg-white rounded-xl shadow-2xl p-6 sm:p-8 lg:p-10 mb-8 transform transition-all duration-300 hover:scale-[1.01] hover:shadow-3xl">
      <AppHeader />
      
      <GitHubReposLoader
        username={githubUsername}
        setUsername={setGithubUsername}
        onLoadRepos={loadGitHubRepos}
        loading={loading}
      />

      <LoadedReposDisplay repos={reposData} isLoaded={isLoaded} />
      
      <QuestionInput
        question={question}
        setQuestion={setQuestion}
        onAskAssistant={askAssistant}
        loading={loading}
        isLoaded={isLoaded}
      />

      <AssistantAnswerDisplay 
        answer={answer} 
        isLoaded={isLoaded} 
      />
    </div>

    <AppFooter />
  </div>
);

// 主應用組件
export default function App() {
  // 使用 hook 獲取所有需要的狀態和方法
  const appProps = useApp();
  
  // 將所有 props 傳遞給 UI 組件
  return <AppUI {...appProps} />;
}
