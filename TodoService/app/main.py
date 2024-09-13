from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import todo
from . import models
from .database import *

models.Base.metadata.create_all(bind=engine)

application = FastAPI(
    title="Todo Service",
    description="todo docs",
    docs_url=None,
    redoc_url="/docs",
)
application.include_router(todo.router)

@application.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")