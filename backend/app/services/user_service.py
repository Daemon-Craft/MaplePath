from typing import Optional
from fastapi import HTTPException, status
from firebase_admin import auth
from app.models.user import users
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.db.database import database


class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> dict:
        """Create a new user"""
        # Check if user already exists
        existing_user = await database.fetch_one(
            users.select().where(users.c.email == user_data.email)
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash password if provided
        hashed_password = None
        if user_data.password:
            hashed_password = get_password_hash(user_data.password)

        # Insert new user
        query = users.insert().values(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            firebase_uid=user_data.firebase_uid,
            phone_number=user_data.phone_number,
            is_verified=bool(user_data.firebase_uid)  # Auto-verify Google users
        )
        user_id = await database.execute(query)

        # Return created user
        return await UserService.get_user_by_id(user_id)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[dict]:
        """Get user by ID"""
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_firebase_uid(firebase_uid: str) -> Optional[dict]:
        """Get user by Firebase UID"""
        query = users.select().where(users.c.firebase_uid == firebase_uid)
        return await database.fetch_one(query)

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[dict]:
        """Authenticate user with email and password"""
        user = await UserService.get_user_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None  # User registered with Google
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def authenticate_google_user(firebase_token: str) -> dict:
        """Authenticate user with Google Firebase token"""
        try:
            # Verify Firebase token
            decoded_token = auth.verify_id_token(firebase_token)
            firebase_uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name')

            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email not found in Firebase token"
                )

            # Check if user exists
            user = await UserService.get_user_by_firebase_uid(firebase_uid)

            if not user:
                # Create new user for Google sign-in
                user_data = UserCreate(
                    email=email,
                    full_name=name,
                    firebase_uid=firebase_uid
                )
                user = await UserService.create_user(user_data)

            return user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Firebase token: {str(e)}"
            )

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> dict:
        """Update user profile"""
        # Check if user exists
        existing_user = await UserService.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update user
        update_data = user_data.dict(exclude_unset=True)
        if update_data:
            query = users.update().where(users.c.id == user_id).values(**update_data)
            await database.execute(query)

        # Return updated user
        return await UserService.get_user_by_id(user_id)
