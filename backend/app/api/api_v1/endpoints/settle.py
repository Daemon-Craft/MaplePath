from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.settle import (
    SettleRegion, SettleRegionCreate, SettleRegionUpdate,
    SettlePurpose, SettlePurposeCreate, SettlePurposeUpdate,
    UserSettlePurpose, UserSettlePurposeCreate, UserSettlePurposeUpdate
)
from app.services.settle_service import (
    SettleRegionService,
    SettlePurposeService,
    UserSettlePurposeService
)
from app.api.api_v1.endpoints.auth import get_current_user

router = APIRouter()


# ============= Settle Regions Endpoints =============

@router.post("/regions", response_model=SettleRegion, status_code=status.HTTP_201_CREATED)
async def create_region(
    region_data: SettleRegionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new settle region"""
    return await SettleRegionService.create_region(region_data)


@router.get("/regions", response_model=List[SettleRegion])
async def get_all_regions():
    """Get all settle regions"""
    return await SettleRegionService.get_all_regions()


@router.get("/regions/{region_id}", response_model=SettleRegion)
async def get_region(region_id: int):
    """Get a specific settle region"""
    return await SettleRegionService.get_region_by_id(region_id)


@router.put("/regions/{region_id}", response_model=SettleRegion)
async def update_region(
    region_id: int,
    region_data: SettleRegionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a settle region"""
    return await SettleRegionService.update_region(region_id, region_data)


@router.delete("/regions/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(
    region_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a settle region"""
    await SettleRegionService.delete_region(region_id)


# ============= Settle Purposes Endpoints =============

@router.post("/purposes", response_model=SettlePurpose, status_code=status.HTTP_201_CREATED)
async def create_purpose(
    purpose_data: SettlePurposeCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new settle purpose"""
    return await SettlePurposeService.create_purpose(purpose_data)


@router.get("/purposes", response_model=List[SettlePurpose])
async def get_all_purposes():
    """Get all settle purposes"""
    return await SettlePurposeService.get_all_purposes()


@router.get("/purposes/{purpose_id}", response_model=SettlePurpose)
async def get_purpose(purpose_id: int):
    """Get a specific settle purpose"""
    return await SettlePurposeService.get_purpose_by_id(purpose_id)


@router.get("/regions/{region_id}/purposes", response_model=List[SettlePurpose])
async def get_purposes_by_region(region_id: int):
    """Get all purposes for a specific region"""
    return await SettlePurposeService.get_purposes_by_region(region_id)


@router.put("/purposes/{purpose_id}", response_model=SettlePurpose)
async def update_purpose(
    purpose_id: int,
    purpose_data: SettlePurposeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a settle purpose"""
    return await SettlePurposeService.update_purpose(purpose_id, purpose_data)


@router.delete("/purposes/{purpose_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_purpose(
    purpose_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a settle purpose"""
    await SettlePurposeService.delete_purpose(purpose_id)


# ============= User Settle Purposes Endpoints =============

@router.post("/user-purposes", response_model=UserSettlePurpose, status_code=status.HTTP_201_CREATED)
async def create_user_purpose(
    purpose_data: UserSettlePurposeCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new user settle purpose (assign a purpose to the current user)"""
    return await UserSettlePurposeService.create_user_purpose(current_user["id"], purpose_data)


@router.get("/user-purposes", response_model=List[UserSettlePurpose])
async def get_user_purposes(current_user: dict = Depends(get_current_user)):
    """Get all purposes for the current user"""
    return await UserSettlePurposeService.get_user_purposes(current_user["id"])


@router.get("/user-purposes/{user_purpose_id}", response_model=UserSettlePurpose)
async def get_user_purpose(
    user_purpose_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific user purpose"""
    return await UserSettlePurposeService.get_user_purpose_by_id(user_purpose_id)


@router.put("/user-purposes/{user_purpose_id}", response_model=UserSettlePurpose)
async def update_user_purpose(
    user_purpose_id: int,
    purpose_data: UserSettlePurposeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a user purpose (status and progression)"""
    return await UserSettlePurposeService.update_user_purpose(
        user_purpose_id,
        current_user["id"],
        purpose_data
    )


@router.delete("/user-purposes/{user_purpose_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_purpose(
    user_purpose_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a user purpose"""
    await UserSettlePurposeService.delete_user_purpose(user_purpose_id, current_user["id"])
