from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import users, models, auth, workspaces
from core.schemas.utils import Message

app = FastAPI(
    title="Zebbra API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Message)
async def root():
    """
    Heartbeat endpoint to check if server is running.
    """
    return {"message": "Hello Zebbra!"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(models.router)
app.include_router(workspaces.router)
