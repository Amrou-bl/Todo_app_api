from fastapi import APIRouter, Depends, HTTPException, status, Response, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import database, schemas, models
from ..auth_utils import *
import requests



def get_todos(db: Session, limit: int, search: str , user_id: str, offset: int):
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Id is required"
        )
        
    if not isinstance(search, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search parameter must be a string"
        )
        
    page_number = (offset // limit) + 1
    
    todos = db.query(models.Todo)\
              .filter(models.Todo.user_id == user_id)\
              .filter(models.Todo.title.contains(search))\
              .limit(limit)\
              .offset(offset)\
              .all()
    
    
    
    return {
        "page_number": page_number,
        "todos": todos
    }
    
    
def create_todo(todo: schemas.TodoCreate, db: Session, user_id: str):
    
    if not todo.title or not todo.description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and description cannot be empty"
        )

    new_todo = models.Todo(title= todo.title, description = todo.description, user_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo



def update_todo(*, todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(database.get_db), user_id: str):
    
    if todo_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID"
        )
    
    todo_query = db.query(models.Todo).filter(models.Todo.id == id, models.Todo.user_id == user_id)
    
    todo_to_update = todo_query.first()
    
    if todo_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id : {todo_id} does not exist or you do not have permission to update it")

    if not todo.title or not todo.description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and description cannot be empty"
        )        
    todo_query.update(todo.model_dump(), synchronize_session=False)
    db.commit()
    
    return todo_query.first()



def delete_todo(todo_id: int, db:Session, user_id: str):
    
    if todo_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID"
        )
    
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id)
    
    todo_to_delete = todo_query.first()
    
    if todo_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"todo with id: {todo_id} not found")
    
    todo_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)