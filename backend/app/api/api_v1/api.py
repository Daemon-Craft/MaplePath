from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, settle, cv

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include user management routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include settle routes
api_router.include_router(settle.router, prefix="/settle", tags=["settle"])

# Include CV builder routes
api_router.include_router(cv.router, prefix="/cv", tags=["cv-builder"])
