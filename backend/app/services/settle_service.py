from typing import Optional, List
from fastapi import HTTPException, status
from app.models.user import settle_regions, settle_purposes, user_settle_purposes
from app.schemas.settle import (
    SettleRegionCreate, SettleRegionUpdate,
    SettlePurposeCreate, SettlePurposeUpdate,
    UserSettlePurposeCreate, UserSettlePurposeUpdate
)
from app.db.database import database


class SettleRegionService:
    @staticmethod
    async def create_region(region_data: SettleRegionCreate) -> dict:
        """Create a new settle region"""
        existing_region = await database.fetch_one(
            settle_regions.select().where(settle_regions.c.region_name == region_data.region_name)
        )
        if existing_region:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Region with this name already exists"
            )

        query = settle_regions.insert().values(region_name=region_data.region_name)
        region_id = await database.execute(query)
        return await SettleRegionService.get_region_by_id(region_id)

    @staticmethod
    async def get_region_by_id(region_id: int) -> Optional[dict]:
        """Get region by ID"""
        query = settle_regions.select().where(settle_regions.c.id == region_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all_regions() -> List[dict]:
        """Get all regions"""
        query = settle_regions.select()
        return await database.fetch_all(query)

    @staticmethod
    async def update_region(region_id: int, region_data: SettleRegionUpdate) -> dict:
        """Update a region"""
        existing_region = await SettleRegionService.get_region_by_id(region_id)
        if not existing_region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region not found"
            )

        update_data = region_data.dict(exclude_unset=True)
        if update_data:
            query = settle_regions.update().where(settle_regions.c.id == region_id).values(**update_data)
            await database.execute(query)

        return await SettleRegionService.get_region_by_id(region_id)

    @staticmethod
    async def delete_region(region_id: int) -> bool:
        """Delete a region"""
        existing_region = await SettleRegionService.get_region_by_id(region_id)
        if not existing_region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region not found"
            )

        query = settle_regions.delete().where(settle_regions.c.id == region_id)
        await database.execute(query)
        return True


class SettlePurposeService:
    @staticmethod
    async def create_purpose(purpose_data: SettlePurposeCreate) -> dict:
        """Create a new settle purpose"""
        region = await SettleRegionService.get_region_by_id(purpose_data.region_id)
        if not region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region not found"
            )

        query = settle_purposes.insert().values(
            region_id=purpose_data.region_id,
            purpose_name=purpose_data.purpose_name,
            description=purpose_data.description
        )
        purpose_id = await database.execute(query)
        return await SettlePurposeService.get_purpose_by_id(purpose_id)

    @staticmethod
    async def get_purpose_by_id(purpose_id: int) -> Optional[dict]:
        """Get purpose by ID"""
        query = settle_purposes.select().where(settle_purposes.c.id == purpose_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all_purposes() -> List[dict]:
        """Get all purposes"""
        query = settle_purposes.select()
        return await database.fetch_all(query)

    @staticmethod
    async def get_purposes_by_region(region_id: int) -> List[dict]:
        """Get all purposes for a specific region"""
        query = settle_purposes.select().where(settle_purposes.c.region_id == region_id)
        return await database.fetch_all(query)

    @staticmethod
    async def update_purpose(purpose_id: int, purpose_data: SettlePurposeUpdate) -> dict:
        """Update a purpose"""
        existing_purpose = await SettlePurposeService.get_purpose_by_id(purpose_id)
        if not existing_purpose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purpose not found"
            )

        update_data = purpose_data.dict(exclude_unset=True)
        if update_data.get("region_id"):
            region = await SettleRegionService.get_region_by_id(update_data["region_id"])
            if not region:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Region not found"
                )

        if update_data:
            query = settle_purposes.update().where(settle_purposes.c.id == purpose_id).values(**update_data)
            await database.execute(query)

        return await SettlePurposeService.get_purpose_by_id(purpose_id)

    @staticmethod
    async def delete_purpose(purpose_id: int) -> bool:
        """Delete a purpose"""
        existing_purpose = await SettlePurposeService.get_purpose_by_id(purpose_id)
        if not existing_purpose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purpose not found"
            )

        query = settle_purposes.delete().where(settle_purposes.c.id == purpose_id)
        await database.execute(query)
        return True


class UserSettlePurposeService:
    @staticmethod
    async def create_user_purpose(user_id: int, purpose_data: UserSettlePurposeCreate) -> dict:
        """Create a new user settle purpose"""
        purpose = await SettlePurposeService.get_purpose_by_id(purpose_data.settle_purpose_id)
        if not purpose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settle purpose not found"
            )

        existing = await database.fetch_one(
            user_settle_purposes.select().where(
                (user_settle_purposes.c.user_id == user_id) &
                (user_settle_purposes.c.settle_purpose_id == purpose_data.settle_purpose_id)
            )
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already assigned to this purpose"
            )

        query = user_settle_purposes.insert().values(
            user_id=user_id,
            settle_purpose_id=purpose_data.settle_purpose_id,
            status=purpose_data.status or "pending",
            progression=purpose_data.progression or 0
        )
        user_purpose_id = await database.execute(query)
        return await UserSettlePurposeService.get_user_purpose_by_id(user_purpose_id)

    @staticmethod
    async def get_user_purpose_by_id(user_purpose_id: int) -> Optional[dict]:
        """Get user purpose by ID"""
        query = user_settle_purposes.select().where(user_settle_purposes.c.id == user_purpose_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_purposes(user_id: int) -> List[dict]:
        """Get all purposes for a specific user"""
        query = user_settle_purposes.select().where(user_settle_purposes.c.user_id == user_id)
        return await database.fetch_all(query)

    @staticmethod
    async def update_user_purpose(user_purpose_id: int, user_id: int, purpose_data: UserSettlePurposeUpdate) -> dict:
        """Update a user purpose"""
        existing = await UserSettlePurposeService.get_user_purpose_by_id(user_purpose_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User purpose not found"
            )

        if existing["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this purpose"
            )

        update_data = purpose_data.dict(exclude_unset=True)
        if update_data.get("progression") is not None:
            if not 0 <= update_data["progression"] <= 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Progression must be between 0 and 100"
                )

        if update_data:
            query = user_settle_purposes.update().where(user_settle_purposes.c.id == user_purpose_id).values(**update_data)
            await database.execute(query)

        return await UserSettlePurposeService.get_user_purpose_by_id(user_purpose_id)

    @staticmethod
    async def delete_user_purpose(user_purpose_id: int, user_id: int) -> bool:
        """Delete a user purpose"""
        existing = await UserSettlePurposeService.get_user_purpose_by_id(user_purpose_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User purpose not found"
            )

        if existing["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this purpose"
            )

        query = user_settle_purposes.delete().where(user_settle_purposes.c.id == user_purpose_id)
        await database.execute(query)
        return True
