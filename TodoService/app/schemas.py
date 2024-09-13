from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class TodoCreate(BaseModel):
    title: str 
    description: str 
    

class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    user_id: int
    
class TodoUpdate(TodoCreate):
    completed: bool 
    
class PaginatedTodosResponse(BaseModel):
    page_number: int
    todos: List[TodoOut]
