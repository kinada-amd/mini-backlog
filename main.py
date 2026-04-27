from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int             # 削除するためにIDを追加
    title: str
    due_date: date
    member: str
    priority: str
    importance: str
    status: str = "未対応"

tasks = []
id_counter = 1

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pro Task Manager</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-[#f4f5f7] font-sans text-gray-800">
        <nav class="bg-blue-900 text-white p-4 shadow-lg mb-6">
            <div class="max-w-5xl mx-auto flex justify-between items-center">
                <h1 class="text-xl font-bold italic tracking-wider">PROJECT MANAGER</h1>
                <span class="text-sm opacity-75">Work Management</span>
            </div>
        </nav>

        <div class="max-w-5xl mx-auto px-4 grid md:grid-cols-3 gap-8">
            <div class="md:col-span-1">
                <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 sticky top-4">
                    <h2 class="text-lg font-bold mb-4 border-b pb-2">新規課題登録</h2>
                    <div class="space-y-4">
                        <div>
                            <label class="text-xs font-bold text-gray-500 uppercase">課題内容</label>
                            <input id="title" type="text" class="w-full border-2 border-gray-100 p-2 rounded focus:border-blue-500 outline-none transition">
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="text-xs font-bold text-gray-500 uppercase">期日</label>
                                <input id="due_date" type="date" class="w-full border-2 border-gray-100 p-2 rounded text-sm">
                            </div>
                            <div>
                                <label class="text-xs font-bold text-gray-500 uppercase">担当者</label>
                                <input id="member" type="text" class="w-full border-2 border-gray-100 p-2 rounded text-sm" placeholder="名前">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="text-xs font-bold text-gray-500 uppercase">優先度</label>
                                <select id="priority" class="w-full border-2 border-gray-100 p-2 rounded text-sm bg-white">
                                    <option value="高">🔥 高</option>
                                    <option value="中" selected>⚡️ 中</option>
                                    <option value="低">💤 低</option>
                                </select>
                            </div>
                            <div>
                                <label class="text-xs font-bold text-gray-500 uppercase">重要度</label>
                                <select id="importance" class="w-full border-2 border-gray-100 p-2 rounded text-sm bg-white">
                                    <option value="A">Class A</option>
                                    <option value="B" selected>Class B</option>
                                    <option value="C">Class C</option>
                                </select>
                            </div>
                        </div>
                        <button onclick="addTask()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded shadow-md transition transform active:scale-95">課題を追加する</button>
                    </div>
                </div>
            </div>

            <div class="md:col-span-2">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-bold">課題一覧</h2>
                    <span id="taskCount" class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-xs font-bold">0 Tasks</span>
                </div>
                <div id="taskList" class="space-y-3">
                    </div>
            </div>
        </div>

        <script>
            async function loadTasks() {
                const res = await fetch('/tasks');
                const data = await res.json();
                const list = document.getElementById('taskList');
                document.getElementById('taskCount').innerText = `${data.length} Tasks`;
                list.innerHTML = '';
                
                data.forEach(task => {
                    const priorityClass = task.priority === '高' ? 'bg-red-500' : (task.priority === '中' ? 'bg-yellow-500' : 'bg-green-500');
                    list.innerHTML += `
                        <div class="bg-white border-l-4 ${task.priority === '高' ? 'border-red-500' : 'border-blue-400'} p-4 rounded shadow-sm hover:shadow-md transition group">
                            <div class="flex justify-between items-start">
                                <div>
                                    <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">#ID-${task.id}</span>
                                    <h3 class="font-bold text-gray-800 text-lg">${task.title}</h3>
                                </div>
                                <button onclick="deleteTask(${task.id})" class="text-gray-300 hover:text-red-500 transition px-2 py-1">
                                    <i class="fas fa-trash-can"></i>
                                </button>
                            </div>
                            <div class="mt-4 flex flex-wrap gap-3 items-center text-xs font-bold">
                                <span class="${priorityClass} text-white px-2 py-0.5 rounded uppercase">優先度 ${task.priority}</span>
                                <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded border border-gray-200"><i class="far fa-calendar mr-1"></i>${task.due_date}</span>
                                <span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded border border-gray-200"><i class="far fa-user mr-1"></i>${task.member}</span>
                                <span class="ml-auto text-blue-600 bg-blue-50 px-2 py-0.5 rounded italic">重要度: ${task.importance}</span>
                            </div>
                        </div>
                    `;
                });
            }

            async function addTask() {
                const titleInput = document.getElementById('title');
                if(!titleInput.value) return alert('内容を入力してください');
                
                const task = {
                    title: titleInput.value,
                    due_date: document.getElementById('due_date').value || '2026-12-31',
                    member: document.getElementById('member').value || '未設定',
                    priority: document.getElementById('priority').value,
                    importance: document.getElementById('importance').value
                };
                await fetch('/tasks', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(task)
                });
                titleInput.value = '';
                loadTasks();
            }

            async function deleteTask(id) {
                if(!confirm('この課題を削除しますか？')) return;
                await fetch(`/tasks/${id}`, { method: 'DELETE' });
                loadTasks();
            }

            loadTasks();
        </script>
    </body>
    </html>
    """

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task_data: dict):
    global id_counter
    task_data["id"] = id_counter
    tasks.append(task_data)
    id_counter += 1
    return {"status": "ok"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"status": "ok"}
