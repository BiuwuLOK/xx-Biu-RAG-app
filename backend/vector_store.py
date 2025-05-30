"""
向量儲存與分塊邏輯模組。
提供記憶體內的向量儲存與文本分塊功能。
"""
from typing import List, Dict

GEMINI_API_KEY = ""  # Canvas 會自動填充此值

# 模擬的向量儲存 (in-memory)
in_memory_vector_store: List[Dict[str, str]] = []
# 儲存已載入的專案數據
loaded_projects_metadata: List[Dict[str, str]] = []

def chunk_text(text: str, chunk_size: int = 500):
    """將文本分割成指定大小的塊"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
