from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI()

# タスクの型
class Task(BaseModel):
    title: str
    due_date: date
    member: str
    priority: str
    importance: str
    status: str = "未対応"

# 仮のデータ保存場所
tasks = []

# --- 画面（HTML）を表示する設定 ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # ここに「今風のデザイン」のHTMLを直接書きます
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Backlog</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 min-h-screen p-4">
        <div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-6">
            <h1 class="text-2xl font-bold text-gray-800 mb-6">📝 タスク管理ツール</h1>
            
            <div class="space-y-4 mb-10">
                <input id="title" type="text" placeholder="タスク内容" class="w-full border p-2 rounded-lg">
                <div class="grid grid-cols-2 gap-4">
                    <input id="due_date" type="date" class="border p-2 rounded-lg">
                    <input id="member" type="text" placeholder="担当者" class="border p-2 rounded-lg">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <select id="priority" class="border p-2 rounded-lg">
                        <option value="高">優先度：高</option>
                        <option value="中" selected>優先度：中</option>
                        <option value="低">優先度：低</option>
                    </select>
                    <select id="importance" class="border p-2 rounded-lg">
                        <option value="A">重要度：A</option>
                        <option value="B" selected>重要度：B</option>
                        <option value="C">重要度：C</option>
                    </select>
                </div>
                <button onclick="addTask()" class="w-full bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700">タスクを追加</button>
            </div>

            <hr class="my-6">

            <div id="taskList" class="space-y-4">
                </div>
        </div>

        <script>
            async function loadTasks() {
                const res = await fetch('/tasks');
                const data = await res.json();
                const list = document.getElementById('taskList');
                list.innerHTML = '';
                data.forEach(task => {
                    const priorityColor = task.priority === '高' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800';
                    list.innerHTML += `
                        <div class="border p-4 rounded-lg shadow-sm bg-gray-50">
                            <div class="flex justify-between items-start">
                                <h3 class="font-bold text-lg">${task.title}</h3>
                                <span class="px-2 py-1 text-xs font-semibold rounded-full ${priorityColor}">${task.priority}</span>
                            </div>
                            <div class="text-sm text-gray-600 mt-2">
                                <p>📅 期限: ${task.due_date} | 👤: ${task.member}</p>
                                <p>⭐️ 重要度: ${task.importance} | 状態: ${task.status}</p>
                            </div>
                        </div>
                    `;
                });
            }

            async function addTask() {
                const task = {
                    title: document.getElementById('title').value,
                    due_date: document.getElementById('due_date').value,
                    member: document.getElementById('member').value,
                    priority: document.getElementById('priority').value,
                    importance: document.getElementById('importance').value
                };
                await fetch('/tasks', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(task)
                });
                loadTasks(); // 再読み込み
            }

            loadTasks(); // 最初に読み込む
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Success"}
