# main.py (FastAPI 後端應用程式)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx # 用於異步 HTTP 請求
import base64
import asyncio # 用於異步延遲

# 引入 LLM API 相關配置
# 在 Canvas 環境中，apiKey 會在運行時自動提供
# 在本地運行時，您可能需要在此處填寫您的 Gemini API 金鑰
# 例如：GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_API_KEY = "" # Canvas 會自動填充此值

app = FastAPI(
    title="GitHub RAG 助手後端",
    description="提供 GitHub 專案數據載入和基於 RAG 的 LLM 問答服務",
    version="1.0.0"
)

# 啟用 CORS，允許前端應用程式從不同來源訪問
# 在生產環境中，請將 allow_origins 限制為您的前端域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，本地開發方便
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有請求頭
)

# 模擬的向量儲存 (in-memory)，在實際應用中會是真正的向量資料庫
# 儲存格式: [{"content": "chunk text", "project": "project_name"}]
in_memory_vector_store = []

# 儲存已載入的專案數據，方便後續檢索時參考
loaded_projects_metadata = []

# --- Pydantic 模型用於請求和響應驗證 ---
class GitHubLoadRequest(BaseModel):
    username: str

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# --- 輔助函數 ---
async def fetch_github_repos(username: str):
    """從 GitHub API 獲取用戶的所有公開倉庫列表"""
    url = f"https://api.github.com/users/{username}/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status() # 如果請求失敗，拋出 HTTPXException
        return response.json()

async def fetch_readme_content(username: str, repo_name: str):
    """從 GitHub API 獲取指定倉庫的 README.md 內容 (Base64 編碼)"""
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if 'content' in data:
            # Base64 解碼內容
            return base64.b64decode(data['content']).decode('utf-8')
        return None

def chunk_text(text: str, chunk_size: int = 500):
    """將文本分割成指定大小的塊"""
    # 簡單的分塊，實際 RAG 會使用更智能的分詞器和分塊策略
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

async def call_gemini_llm(prompt: str):
    """呼叫 Gemini LLM API 生成回答"""
    # 這裡的 API 呼叫邏輯與前端類似，確保使用 Canvas 環境提供的 API_KEY
    # 在本地運行時，請確保 GEMINI_API_KEY 已設定
    api_key = GEMINI_API_KEY # Canvas 會自動填充

    if not api_key:
        print("警告：未提供 Gemini API 金鑰。請在本地環境中設定 GEMINI_API_KEY。")
        # 如果沒有 API 金鑰，可以返回一個模擬響應或拋出錯誤
        return "很抱歉，LLM 服務目前無法訪問，請檢查 API 金鑰配置。"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    async with httpx.AsyncClient(timeout=60.0) as client: # 增加超時時間
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status() # 檢查 HTTP 狀態碼
            result = response.json()

            if result.get('candidates') and len(result['candidates']) > 0 and \
               result['candidates'][0].get('content') and \
               result['candidates'][0]['content'].get('parts') and \
               len(result['candidates'][0]['content']['parts']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"LLM 返回無效結構: {result}")
                return "抱歉，LLM 未能生成有效回答。"
        except httpx.HTTPStatusError as e:
            print(f"LLM API HTTP 錯誤: {e.response.status_code} - {e.response.text}")
            return f"LLM 服務錯誤：{e.response.status_code}。請稍後再試。"
        except httpx.RequestError as e:
            print(f"LLM API 請求錯誤: {e}")
            return "無法連接到 LLM 服務，請檢查網絡或 API 狀態。"
        except Exception as e:
            print(f"呼叫 LLM 時發生意外錯誤: {e}")
            return "呼叫 LLM 時發生未知錯誤。"

# --- API 端點 ---

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
                    loaded_projects_metadata.append({"name": repo['name'], "content": readme_content})
                    chunks = chunk_text(readme_content)
                    for chunk in chunks:
                        in_memory_vector_store.append({"content": chunk, "project": repo['name']})
                else:
                    print(f"警告: 專案 {repo['name']} 沒有可讀取的 README.md 內容。")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    print(f"警告: 專案 {repo['name']} 沒有 README.md 文件。")
                elif e.response.status_code == 403:
                    raise HTTPException(status_code=403, detail="GitHub API 速率限制已達到。請稍後再試。")
                else:
                    print(f"獲取專案 {repo['name']} README.md 時發生 HTTP 錯誤: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                print(f"獲取專案 {repo['name']} README.md 時發生意外錯誤: {e}")
            finally:
                await asyncio.sleep(0.5) # 請求間隔 500 毫秒，避免觸發 GitHub 速率限制

        if not in_memory_vector_store:
            raise HTTPException(status_code=404, detail="未找到任何可用的 GitHub 專案 README 內容。請確保用戶名正確且專案有 README 文件。")

        return {"message": f"成功載入 {len(loaded_projects_metadata)} 個專案的數據！", "projects_count": len(loaded_projects_metadata)}

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"GitHub 用戶 '{request.username}' 不存在或沒有公開倉庫。")
        elif e.response.status_code == 403:
            raise HTTPException(status_code=403, detail="GitHub API 速率限制已達到。請稍後再試。")
        else:
            raise HTTPException(status_code=e.response.status_code, detail=f"獲取 GitHub 倉庫時發生錯誤: {e.response.status_code} {e.response.text}")
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
    keywords = question.lower().split(/\s+/).filter(lambda w: len(w) > 2)
    relevant_chunks = []
    
    for item in in_memory_vector_store:
        lower_content = item["content"].lower()
        if any(keyword in lower_content for keyword in keywords):
            relevant_chunks.append({"content": item["content"], "project": item["project"]})
            if len(relevant_chunks) >= 5: # 限制檢索到的塊數量
                break
    
    context = ""
    if relevant_chunks:
        context = "\n\n".join([f"專案名稱: {rc['project']}\n內容片段: {rc['content']}" for rc in relevant_chunks])
    else:
        # 如果沒有找到相關內容，直接返回預設提示
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
