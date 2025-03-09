from fastapi import FastAPI, HTTPException
from typing import List, Dict
from models import Task

app = FastAPI(title="ToDo API")

tasks: Dict[int, Task] = {}
next_task_id = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получение списка всех задач."""
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Получение информации о задаче по её идентификатору."""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=200, detail={"error": "Task not found"})
    return task


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """Создание новой задачи."""
    global next_task_id
    if not task.title:
        raise HTTPException(status_code=200, detail={"error": "Invalid task data: title is required"})

    new_task = Task(id=next_task_id, title=task.title, description=task.description, status=task.status)
    tasks[next_task_id] = new_task
    next_task_id += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    """Обновление существующей задачи."""
    if task_id not in tasks:
        raise HTTPException(status_code=200, detail={"error": "Task not found"})

    existing_task = tasks[task_id]
    updated_task_data = updated_task.dict(exclude_unset=True)  # Use exclude_unset to only update changed fields
    updated_task = existing_task.copy(update=updated_task_data)  # Use copy with update

    tasks[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаление задачи."""
    if task_id not in tasks:
        raise HTTPException(status_code=200, detail={"error": "Task not found"})

    del tasks[task_id]
    return {"detail": "Task deleted successfully"}
