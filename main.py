from fastapi import FastAPI
from .models.admin import Base
from .config.database import engine
from .routers import (
    user,personal
)

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(personal.router)

@app.get('/')
async def root():
    return {'sms':'hello_word'}