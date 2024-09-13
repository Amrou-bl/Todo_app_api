from fastapi import APIRouter, Depends, status, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import database, schemas
from ..services import todo_service
from ..auth_utils import *

router = APIRouter(tags=['Todo Service'])


@router.get("/api/todo", response_model=schemas.PaginatedTodosResponse,
            summary="List all the todos")
async def get_todos(db: Session = Depends(database.get_db),
                    limit: int = Query(10, gt=0, le=20, description="Number of todos to return"),
                    search: Optional[str] = Query("", description="Query string for the items to search in the database"),
                    authorization: str = Header(None),
                    offset: int = Query(0,ge=0, description="Number of todos to skip")):
    """
    Retrieve a paginated list of todo items for the authenticated user.

    **Description:**
    - This endpoint fetches a list of todo items associated with the authenticated user.
    - It supports pagination through the `limit` and `offset` parameters.
    - Users can filter todos using the `search` parameter to find specific items based on a query string.

    **Parameters:**
    - `db` (Session, optional): The database session dependency.
    - `limit` (int, optional): The maximum number of todos to return. Must be greater than 0 and less than or equal to 20. Defaults to 10.
    - `search` (str, optional): A query string to filter todos based on their title or description. Defaults to an empty string, which returns all todos.
    - `authorization` (str): The Authorization header containing the JWT token in the format "Bearer <token>".
    - `offset` (int, optional): The number of todos to skip for pagination. Must be greater than or equal to 0. Defaults to 0.

    **Returns:**
    - `PaginatedTodosResponse`: A model containing:
        - `total`: (int) The total number of todos for the user.
        - `todos`: (List[Todo]) A list of todo items returned for the current page.

    **Responses:**
    - **200 OK**: Returns a paginated list of todos with the total count and the todos data.
    - **401 Unauthorized**: Returned if the token is missing, invalid, or user verification fails.

    **Example Response:**

    ```json
    {
      "total": 25,
      "todos": [
        {
          "id": 1,
          "title": "Buy groceries",
          "description": "Milk, Bread, Eggs",
          "user_id": "12345"
        },
        {
          "id": 2,
          "title": "Read book",
          "description": "Finish reading the novel",
          "user_id": "12345"
        }
      ]
    }
    ```
    - `total`: The total number of todos available for the user.
    - `todos`: A list of todo items for the current page, filtered and paginated according to the provided parameters.
    """

    user_id = await get_verified_user(authorization)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User verification failed"
        )
    return todo_service.get_todos(db, limit, search, user_id, offset)



@router.post("/api/todo",status_code=status.HTTP_201_CREATED,
             summary="Create a New Todo")
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), authorization: str = Header(None)):
    """
    Create a new Todo item for the authenticated user.

    **Description:**
    - This endpoint allows an authenticated user to create a new todo item.
    - It requires a valid JWT token in the Authorization header.
    - The todo item is linked to the user's ID and stored in the database.

    **Parameters:**
    - `todo` (TodoCreate): The todo data containing the title and description.
    - `db` (Session, optional): The database session dependency.
    - `authorization` (str): The Authorization header containing the JWT token in the format "Bearer <token>".

    **Returns:**
    - `Todo`: The created todo item.

    **Responses:**
    - **201 Created**: Returned when the todo item is successfully created.
    - **401 Unauthorized**: Returned if the token is missing or invalid.
    - **400 Bad Request**: Returned if the title or description is missing.

    **Example Response:**

    ```json
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs",
      "user_id": "12345"
    }
    ```
    - `id`: The ID of the created todo item.
    - `title`: The title of the todo item.
    - `description`: The description of the todo item.
    - `user_id`: The ID of the user who created the todo item.
    """
    user_id = await get_verified_user(authorization)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User verification failed"
        )
    return todo_service.create_todo(todo, db, user_id)


@router.put("/api/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT,
             summary="Update a Todo")
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(database.get_db), authorization: str = Header(None)):
    """
    Update an existing Todo item for the authenticated user.

    **Description:**
    - This endpoint allows an authenticated user to update an existing todo item.
    - It requires a valid JWT token in the Authorization header.
    - The todo item must belong to the authenticated user.

    **Parameters:**
    - `todo_id` (int): The ID of the todo item to be updated.
    - `todo` (TodoUpdate): The updated todo data containing the title and description.
    - `db` (Session, optional): The database session dependency.
    - `authorization` (str): The Authorization header containing the JWT token in the format "Bearer <token>".

    **Returns:**
    - `Todo`: The updated todo item.

    **Responses:**
    - **204 No Content**: Returned when the todo item is successfully updated.
    - **401 Unauthorized**: Returned if the token is missing or invalid.
    - **404 Not Found**: Returned if the todo item does not exist or does not belong to the user.
    - **400 Bad Request**: Returned if the title or description is missing.

    **Example Response:**

    ```json
    {}
    ```
    - This response signifies that the todo item was successfully updated with no content returned.
    """
    user_id = await get_verified_user(authorization)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or unauthorized user"
        )
    return todo_service.update_todo(todo_id, todo, db, user_id)


@router.delete("/api/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT,
             summary="Delete a Todo")
async def delete_todo(todo_id: int, db: Session = Depends(database.get_db), authorization: str = Header(None)):

    """
    Delete an existing Todo item for the authenticated user.

    **Description:**
    - This endpoint allows an authenticated user to delete a todo item.
    - It requires a valid JWT token in the Authorization header.
    - The todo item must belong to the authenticated user.

    **Parameters:**
    - `todo_id` (int): The ID of the todo item to be deleted.
    - `db` (Session, optional): The database session dependency.
    - `authorization` (str): The Authorization header containing the JWT token in the format "Bearer <token>".

    **Returns:**
    - `Response`: A response object with no content indicating successful deletion.

    **Responses:**
    - **204 No Content**: Returned when the todo item is successfully deleted.
    - **401 Unauthorized**: Returned if the token is missing or invalid.
    - **404 Not Found**: Returned if the todo item does not exist or does not belong to the user.

    **Example Response:**

    ```json
    {}
    ```
    - This response signifies that the todo item was successfully deleted with no content returned.
    """
    user_id = await get_verified_user(authorization)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or unauthorized user"
        )
    return todo_service.delete_todo(todo_id, db, user_id)