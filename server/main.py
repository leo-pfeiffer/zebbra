from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api import users, models, auth, workspaces, integrations
from api.utils.dependencies import SECRET_KEY
from core.integrations.config import setup_integrations
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

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


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
app.include_router(integrations.router)

# register integration adapters etc.
setup_integrations(app)
