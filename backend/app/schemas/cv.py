from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# Industry schemas
class IndustryBase(BaseModel):
    name: str
    name_fr: Optional[str] = None
    description: Optional[str] = None
    tips: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


class IndustryCreate(IndustryBase):
    pass


class Industry(IndustryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Work Experience schema
class WorkExperience(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None  # YYYY-MM or "Present"
    responsibilities: List[str]
    achievements: Optional[List[str]] = None


# Education schema
class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    location: Optional[str] = None
    graduation_date: str  # YYYY-MM format
    gpa: Optional[str] = None
    honors: Optional[List[str]] = None


# Language schema
class Language(BaseModel):
    language: str
    proficiency: str  # Native, Fluent, Advanced, Intermediate, Basic


# Certification schema
class Certification(BaseModel):
    name: str
    issuing_organization: str
    issue_date: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None


# CV Input for generation
class CVGenerateInput(BaseModel):
    industry_id: int
    job_title: str  # Target job title
    full_name: str
    email: EmailStr
    phone: str
    location: str  # e.g., "Toronto, ON"
    summary: Optional[str] = None  # Professional summary (if empty, AI will generate)
    experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    certifications: Optional[List[Certification]] = None
    languages: Optional[List[Language]] = None
    additional_info: Optional[str] = None  # Any extra info for AI to consider


# CV Response schemas
class UserCVBase(BaseModel):
    title: str
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    languages: Optional[List[Dict[str, Any]]] = None
    format_type: str = "canadian"


class UserCVCreate(UserCVBase):
    industry_id: Optional[int] = None
    cv_content: Dict[str, Any]


class UserCV(UserCVBase):
    id: int
    user_id: int
    industry_id: Optional[int] = None
    cv_content: Dict[str, Any]
    pdf_url: Optional[str] = None
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCVUpdate(BaseModel):
    title: Optional[str] = None
    is_favorite: Optional[bool] = None
    summary: Optional[str] = None
    skills: Optional[List[str]] = None


# CV Generation Response
class CVGenerateResponse(BaseModel):
    cv_id: int
    optimized_summary: str
    optimized_skills: List[str]
    tips: List[str]
    ats_score: int  # ATS compatibility score (0-100)
    suggestions: List[str]


# PDF Export Request
class CVExportRequest(BaseModel):
    cv_id: int
    format: str = "canadian"  # canadian, modern, minimal


# CV Generation History
class CVGenerationHistory(BaseModel):
    id: int
    user_id: int
    cv_id: Optional[int] = None
    industry_id: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    tokens_used: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
