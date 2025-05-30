"""
Pydantic 資料模型模組。
定義 API 請求與回應的資料結構。
"""

from pydantic import BaseModel

class GitHubLoadRequest(BaseModel):
    """GitHub 專案載入請求模型"""
    username: str

class QuestionRequest(BaseModel):
    """提問請求模型"""
    question: str

class AnswerResponse(BaseModel):
    """回答回應模型"""
    answer: str
