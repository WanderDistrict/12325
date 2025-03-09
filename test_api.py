import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"


def test_create_task():
    data = {"title": "Пример задачи", "description": "Описание задачи", "status": "pending"}
    response = requests.post(f"{BASE_URL}/tasks", json=data)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == data["title"]
    assert task["description"] == data["description"]  # Verify description as well.
    assert task["status"] == data["status"]  # Verify status as well.
    return task["id"]


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)


def test_get_task(task_id):
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    if "error" in data:
        assert data["error"] == "Task not found"
    else:
        assert data["id"] == task_id


def test_update_task(task_id):
    data = {"title": "Задача обновлена", "description": "Новое описание", "status": "completed"}
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=data)
    assert response.status_code == 200
    data_response = response.json()
    if "error" in data_response:
        assert data_response["error"] == "Task not found"
    else:
        assert data_response["title"] == data["title"]
        assert data_response["description"] == data["description"]  # Verify description.
        assert data_response["status"] == data["status"]  # Verify status.


def test_delete_task(task_id):
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    data_response = response.json()
    if "error" in data_response:
        assert data_response["error"] == "Task not found"
    else:
        assert data_response["detail"] == "Task deleted successfully"

    # Проверка: повторный запрос должен вернуть ошибку
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data and data["error"] == "Task not found"


if __name__ == "__main__":
    created_task_id = test_create_task()
    test_get_tasks()
    test_get_task(created_task_id)
    test_update_task(created_task_id)
    test_delete_task(created_task_id)
    print("Все тесты пройдены!")
