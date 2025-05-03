from typing import List
from sqlalchemy import or_

from fastapi import HTTPException

from app.db.session import session
from app.models import Task
from app.schemas.task import TaskInRequest


def create_new_task(user_id, task: TaskInRequest) -> Task:
    print("TASK:", task.__dict__)
    new_task = Task(**task.__dict__, owner_id=user_id)
    session.add(new_task)
    session.commit()
    return new_task


def get_task_list(user_id) -> List[Task]:
    tasks = session.query(Task).filter(Task.owner_id == user_id).all()
    return tasks


def get_task_by_id(user_id: int, task_id: int) -> Task:
    task = session.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def search_tasks(user_id: int, query: str) -> List[Task]:
    # Use LIKE with % wildcards to find the substring in either title or description
    search_pattern = f"%{query}%"
    tasks = session.query(Task).filter(
        Task.owner_id == user_id,
        or_(
            Task.title.ilike(search_pattern),
            Task.description.ilike(search_pattern)
        )
    ).all()
    return tasks


def update_task_by_id(user_id: int, task_id: int, task_data: TaskInRequest) -> Task:
    task = session.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task attributes
    for key, value in task_data.__dict__.items():
        setattr(task, key, value)

    session.commit()
    session.refresh(task)
    return task