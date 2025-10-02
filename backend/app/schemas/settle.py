from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Settle Region schemas
class SettleRegionBase(BaseModel):
    region_name: str


class SettleRegionCreate(SettleRegionBase):
    pass


class SettleRegionUpdate(BaseModel):
    region_name: Optional[str] = None


class SettleRegion(SettleRegionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Settle Purpose schemas
class SettlePurposeBase(BaseModel):
    region_id: int
    purpose_name: str
    description: Optional[str] = None


class SettlePurposeCreate(SettlePurposeBase):
    pass


class SettlePurposeUpdate(BaseModel):
    region_id: Optional[int] = None
    purpose_name: Optional[str] = None
    description: Optional[str] = None


class SettlePurpose(SettlePurposeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# User Settle Purpose schemas
class UserSettlePurposeBase(BaseModel):
    user_id: int
    settle_purpose_id: int
    status: str = "pending"  # pending, in_progress, completed
    progression: int = 0  # 0-100


class UserSettlePurposeCreate(BaseModel):
    settle_purpose_id: int
    status: Optional[str] = "pending"
    progression: Optional[int] = 0


class UserSettlePurposeUpdate(BaseModel):
    status: Optional[str] = None
    progression: Optional[int] = None


class UserSettlePurpose(UserSettlePurposeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
