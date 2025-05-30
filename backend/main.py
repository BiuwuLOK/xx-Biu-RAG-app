"""
FastAPI 主應用程式。
負責啟動 API 伺服器、CORS 設定與路由註冊。
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GitHubLoadRequest, QuestionRequest, AnswerResponse
from github_utils import fetch_github_repos, fetch_readme_content
from llm_utils import call_gemini_llm
from vector_store import in_memory_vector_store, loaded_projects_metadata, chunk_text
import asyncio

app = FastAPI(
    title="GitHub RAG 助手後端",
    description="提供 GitHub 專案數據載入和基於 RAG 的 LLM 問答服務",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，本地開發方便
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有請求頭
)

@app.post("/load_github_projects")
async def load_github_projects_endpoint(request: GitHubLoadRequest):
    """
    載入指定 GitHub 用戶的所有公開專案的 README.md 內容。
    將內容分塊並儲存在後端的記憶體中，作為 RAG 的數據源。
    """
    global in_memory_vector_store, loaded_projects_metadata
    in_memory_vector_store = [] # 清空之前的數據
    loaded_projects_metadata = []

    try:
        repos = await fetch_github_repos(request.username)
        
        for repo in repos:
            try:
                readme_content = await fetch_readme_content(request.username, repo['name'])
                if readme_content:
                    # 儲存專案名稱與內容
                    loaded_projects_metadata.append({"name": repo['name'], "content": readme_content})
                    # 將 README 分塊後存入向量儲存
                    chunks = chunk_text(readme_content)
                    for chunk in chunks:
                        in_memory_vector_store.append({"content": chunk, "project": repo['name']})
                else:
                    print(f"警告: 專案 {repo['name']} 沒有可讀取的 README.md 內容。")
            except Exception as e:
                print(f"獲取專案 {repo['name']} README.md 時發生錯誤: {e}")
            finally:
                await asyncio.sleep(0.5) # 請求間隔 500 毫秒，避免觸發 GitHub 速率限制

        if not in_memory_vector_store:
            raise HTTPException(status_code=404, detail="未找到任何可用的 GitHub 專案 README 內容。請確保用戶名正確且專案有 README 文件。")

        return {"message": f"成功載入 {len(loaded_projects_metadata)} 個專案的數據！", "projects_count": len(loaded_projects_metadata)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"載入 GitHub 專案數據時發生意外錯誤: {e}")


@app.post("/ask_assistant", response_model=AnswerResponse)
async def ask_assistant_endpoint(request: QuestionRequest):
    """
    接收問題，從已載入的 GitHub 數據中檢索相關信息，
    並使用 LLM 生成回答。
    """
    if not in_memory_vector_store:
        raise HTTPException(status_code=400, detail="GitHub 專案數據尚未載入。請先載入數據。")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="問題不能為空。")

    # 模擬檢索：簡單的關鍵字匹配
    keywords = [w for w in question.lower().split() if len(w) > 2]
    relevant_chunks = []
    
    for item in in_memory_vector_store:
        lower_content = item["content"].lower()
        if any(keyword in lower_content for keyword in keywords):
            relevant_chunks.append({"content": item["content"], "project": item["project"]})
            if len(relevant_chunks) >= 5: # 限制檢索到的塊數量
                break
    
    context = ""
    if relevant_chunks:
        # 組合檢索到的內容片段作為 LLM 輸入上下文
        context = "\n\n".join([f"專案名稱: {rc['project']}\n內容片段: {rc['content']}" for rc in relevant_chunks])
    else:
        # 沒有找到相關內容時，回傳預設訊息
        return AnswerResponse(answer=f"關於更多訊息請直接訪問作者({request.username})的代碼托管棧(Repository): https://github.com/{request.username}")

    # 構建 LLM 提示
    prompt = f"""你是一個專業的 HR 面試官助手，專門根據提供的 GitHub 專案內容來回答問題。
請根據以下提供的 GitHub 專案內容片段，簡潔、準確地回答問題。
如果提供的內容無法回答問題，請誠實說明。

GitHub 專案內容片段：
---
{context}
---

問題：{question}"""

    llm_answer = await call_gemini_llm(prompt)

    # 檢查 LLM 回答是否為預設的錯誤或無效回答
    if "抱歉，LLM 未能生成有效回答。" in llm_answer or \
       "LLM 服務錯誤" in llm_answer or \
       "無法連接到 LLM 服務" in llm_answer or \
       "呼叫 LLM 時發生未知錯誤" in llm_answer:
        # 如果 LLM 沒有返回有效回答，則返回預設提示
        return AnswerResponse(answer=f"關於更多訊息請直接訪問作者({request.username})的代碼托管棧(Repository): https://github.com/{request.username}")
    
    return AnswerResponse(answer=llm_answer)

# --- 運行應用程式的說明 ---
# 在本地運行此 FastAPI 應用程式：
# 1. 確保您已安裝 Python 和 pip。
# 2. 安裝必要的庫：
#    pip install fastapi uvicorn httpx pydantic
# 3. 將此程式碼儲存為 main.py。
# 4. 在終端機中運行：
#    uvicorn main:app --reload --port 8000
# 應用程式將在 http://127.0.0.1:8000 運行。
