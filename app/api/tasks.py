from typing import List
from fastapi import APIRouter, Request, HTTPException, Query
from ..core.security import check_auth
from ..crud.task import create_new_task, get_task_list, get_task_by_id, update_task_by_id, search_tasks
from app.schemas.task import TaskInRequest, TaskInResponse

router = APIRouter()


@router.post("/tasks", response_model=TaskInResponse, status_code=201)
async def create_task(task: TaskInRequest, request: Request):
    user_id = check_auth(request.headers.get("authorization"))
    new_task = create_new_task(user_id, task)
    return new_task

@router.get("/tasks", response_model=List[TaskInResponse])
async def get_tasks(request: Request):
    user_id = check_auth(request.headers.get("authorization"))
    tasks = get_task_list(user_id)
    return tasks

@router.get("/tasks/search", response_model=List[TaskInResponse])
async def search_task(request: Request, q: str = Query(..., description="Search query string")):
    user_id = check_auth(request.headers.get("authorization"))
    tasks = search_tasks(user_id, q)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskInResponse)
async def get_task(task_id: int, request: Request):
    user_id = check_auth(request.headers.get("authorization"))
    task = get_task_by_id(user_id, task_id)
    return task

@router.put("/tasks/{task_id}", response_model=TaskInResponse)
async def update_task(task_id: int, task: TaskInRequest, request: Request):
    user_id = check_auth(request.headers.get("authorization"))
    updated_task = update_task_by_id(user_id, task_id, task)
    return updated_task