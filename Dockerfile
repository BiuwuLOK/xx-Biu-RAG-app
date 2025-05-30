# 使用官方 Python 基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製後端程式碼與需求檔
COPY backend/ ./backend/
COPY backend/requirements.txt ./backend/requirements.txt

# 安裝依賴
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# 預設啟動 FastAPI 應用
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
