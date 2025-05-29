# xx-Biu-reademe-assis

## 專案簡介

這是一個基於 Retrieval Augmented Generation (RAG) 的應用程式，旨在幫助使用者根據自己的 GitHub 倉庫內容進行問答。後端使用 Python FastAPI 提供 API 服務，前端使用 React 構建使用者介面。

## 功能特色

- 載入指定 GitHub 使用者的公開倉庫數據。
- 根據已載入的倉庫內容回答使用者的問題。
- 清晰的使用者介面展示載入狀態和助手回答。

## 專案結構

```
xx-Biu-RAG-app/
├── LICENSE
├── README.md
├── backend/              # FastAPI 後端
│   ├── main.py           # 後端主程式
│   └── requirements.txt  # 後端依賴
└── frontend/             # React 前端
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.js
    ├── vite.config.js
    ├── public/
    │   └── index.html
    └── src/
        ├── App.jsx
        ├── index.css
        ├── main.jsx
        ├── components/       # React 組件
        │   ├── AppFooter.jsx
        │   ├── AppHeader.jsx
        │   ├── AssistantAnswerDisplay.jsx
        │   ├── GitHubReposLoader.jsx
        │   ├── index.js
        │   ├── LoadedReposDisplay.jsx
        │   ├── MessageBox.jsx
        │   └── QuestionInput.jsx
        ├── config/           # 配置檔案
        │   └── constants.js
        └── hooks/            # 自定義 React Hooks
            ├── hooks.js
            ├── useApp.js
            ├── useAssistant.js
            └── useGitHubReposLoader.js
```

## 環境建置與安裝

請確保您的系統已安裝 Python 3.8+ 和 Node.js。

### 後端設定

1. 進入 `backend` 目錄：
   ```bash
   cd backend
   ```
2. 創建並激活虛擬環境（推薦）：
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. 安裝後端依賴：
   ```bash
   pip install -r requirements.txt
   ```
4. **配置 API 金鑰**：
   後端需要訪問 GitHub API 和一個大型語言模型 (LLM) 的 API（例如 OpenAI）。請在後端環境中設置相應的環境變數或修改配置文件來包含你的 API 金鑰。
   - GitHub Personal Access Token (需要讀取公開倉庫的權限)
   - LLM API Key (例如 OpenAI API Key)

   具體配置方式請參考後端代碼 (`backend/main.py`) 或相關文檔。

### 前端設定

1. 進入 `frontend` 目錄：
   ```bash
   cd frontend
   ```
2. 安裝前端依賴：
   ```bash
   npm install
   ```
3. **配置後端 URL**：
   修改 `frontend/src/config/constants.js` 文件，將 `BACKEND_URL` 設置為你的後端服務地址。
   ```javascript
   export const BACKEND_URL = 'http://localhost:8000'; // 根據你的後端實際運行地址修改
   ```

## 運行應用程式

1. **啟動後端服務**：
   在 `backend` 目錄下，確保虛擬環境已激活，然後運行：
   ```bash
   uvicorn main:app --reload
   ```
   後端服務預設運行在 `http://127.0.0.1:8000`。

2. **啟動前端應用**：
   在 `frontend` 目錄下，運行：
   ```bash
   npm run dev
   ```
   前端應用預設運行在 `http://localhost:5173` (或 Vite 提示的其他端口)。

打開瀏覽器訪問前端地址，即可使用應用程式。

## 使用技術

- **後端**: Python, FastAPI
- **前端**: React, Vite, Tailwind CSS
- **RAG**: (這裡可以補充你使用的 RAG 相關庫或框架，例如 LangChain, LlamaIndex 等)
- **資料庫/向量儲存**: (如果使用了，請補充)
- **LLM**: (請補充你使用的具體 LLM，例如 OpenAI GPT 系列)

## 貢獻

歡迎對此專案做出貢獻。請先 Fork 本倉庫，創建新的分支，提交你的修改，然後發起 Pull Request。

## 許可證

本專案採用 MIT 許可證 - 詳細內容請參閱 [LICENSE](LICENSE) 文件。

## 聯繫方式

如果您有任何問題或建議，歡迎聯繫我。

---

This README Edited with Gemini!
