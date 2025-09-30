from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import firebase_admin
from firebase_admin import credentials

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firebase Admin SDK
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)

    # Connect to database
    await database.connect()
    yield
    # Disconnect from database
    await database.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to MaplePath API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
