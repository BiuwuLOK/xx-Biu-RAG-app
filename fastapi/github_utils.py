"""
GitHub 相關輔助函數模組。
提供與 GitHub API 互動的功能。
"""
import httpx
import base64
import asyncio
from .vector_store import chunk_text, in_memory_vector_store, loaded_projects_metadata

async def fetch_github_repos(username: str):
    """從 GitHub API 獲取用戶的所有公開倉庫列表"""
    url = f"https://api.github.com/users/{username}/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def fetch_readme_content(username: str, repo_name: str):
    """從 GitHub API 獲取指定倉庫的 README.md 內容 (Base64 編碼)"""
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/README.md"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if 'content' in data:
            # Base64 解碼 README.md 內容
            return base64.b64decode(data['content']).decode('utf-8')
        return None
