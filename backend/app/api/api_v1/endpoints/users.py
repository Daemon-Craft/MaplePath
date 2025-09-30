from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import User, UserUpdate, UserCreate
from app.services.user_service import UserService
from app.api.api_v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    """Register a new user with email and password"""
    if not user_data.password and not user_data.firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required for email registration"
        )

    user = await UserService.create_user(user_data)
    return user


@router.get("/profile", response_model=User)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user


@router.put("/profile", response_model=User)
async def update_profile(
    profile_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user's profile"""
    updated_user = await UserService.update_user(current_user.id, profile_data)
    return updated_user


@router.get("/profile/{user_id}", response_model=User)
async def get_user_profile(
    user_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get user profile by ID (for admin or public profiles)"""
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
