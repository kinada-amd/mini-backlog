from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# タスクの型定義
class Task(BaseModel):
    title: str          # 内容
    due_date: date      # 期日
    member: str         # メンバー
    priority: str       # 優先度 (高/中/低)
    importance: str     # 重要度 (A/B/C)
    status: str = "未対応"

# 仮のデータ保存場所
tasks = []

@app.get("/")
def read_root():
    return {"message": "タスク管理API稼働中！"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "タスクを追加しました", "task": task}
