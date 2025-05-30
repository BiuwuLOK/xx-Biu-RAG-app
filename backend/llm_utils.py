"""
LLM 相關輔助函數模組。
提供呼叫 Gemini LLM API 的功能。
"""
import httpx
from .vector_store import GEMINI_API_KEY

async def call_gemini_llm(prompt: str):
    """呼叫 Gemini LLM API 生成回答"""
    api_key = GEMINI_API_KEY
    if not api_key:
        print("警告：未提供 Gemini API 金鑰。請在本地環境中設定 GEMINI_API_KEY。")
        return "很抱歉，LLM 服務目前無法訪問，請檢查 API 金鑰配置。"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # 發送 POST 請求到 Gemini LLM API
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            # 解析 LLM 回傳的內容
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
