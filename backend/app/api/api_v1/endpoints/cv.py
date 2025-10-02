from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from app.schemas.cv import (
    Industry, IndustryCreate,
    CVGenerateInput, CVGenerateResponse,
    UserCV, CVExportRequest
)
from app.services.cv_service import IndustryService, CVService
from app.services.pdf_service import pdf_service
from app.api.api_v1.endpoints.auth import get_current_user

router = APIRouter()


# ============= Industries Endpoints =============

@router.get("/industries", response_model=List[Industry])
async def get_industries():
    """Get all available industries with tips"""
    return await IndustryService.get_all_industries()


@router.get("/industries/{industry_id}", response_model=Industry)
async def get_industry(industry_id: int):
    """Get specific industry details"""
    industry = await IndustryService.get_industry_by_id(industry_id)
    if not industry:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Industry not found")
    return industry


@router.post("/industries", response_model=Industry, status_code=status.HTTP_201_CREATED)
async def create_industry(
    industry_data: IndustryCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new industry (admin only)"""
    return await IndustryService.create_industry(industry_data)


# ============= CV Generation Endpoints =============

@router.post("/generate", response_model=CVGenerateResponse)
async def generate_cv(
    cv_input: CVGenerateInput,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate an optimized CV using Vertex AI

    This endpoint:
    1. Takes user's work experience, education, and skills
    2. Uses Vertex AI to optimize content for the target industry
    3. Provides ATS optimization and tips
    4. Stores the generated CV in the database
    """
    return await CVService.generate_cv(current_user["id"], cv_input)


@router.get("/my-cvs", response_model=List[UserCV])
async def get_my_cvs(current_user: dict = Depends(get_current_user)):
    """Get all CVs created by the current user"""
    return await CVService.get_user_cvs(current_user["id"])


@router.get("/my-cvs/{cv_id}", response_model=UserCV)
async def get_cv(
    cv_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific CV"""
    return await CVService.get_cv_by_id(cv_id, current_user["id"])


@router.delete("/my-cvs/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(
    cv_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a CV"""
    await CVService.delete_cv(cv_id, current_user["id"])


@router.post("/my-cvs/{cv_id}/favorite", response_model=UserCV)
async def toggle_favorite(
    cv_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Toggle favorite status of a CV"""
    return await CVService.toggle_favorite(cv_id, current_user["id"])


# ============= PDF Export Endpoint =============

@router.get("/my-cvs/{cv_id}/export/pdf")
async def export_cv_pdf(
    cv_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Export CV as PDF in Canadian format

    Returns a downloadable PDF file
    """
    # Get the CV
    cv = await CVService.get_cv_by_id(cv_id, current_user["id"])

    # Generate PDF
    pdf_buffer = pdf_service.generate_canadian_cv_pdf(cv)

    # Create filename
    filename = f"CV_{cv['full_name'].replace(' ', '_')}_{cv_id}.pdf"

    # Return as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/my-cvs/{cv_id}/export")
async def export_cv_custom(
    cv_id: int,
    export_request: CVExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Export CV with custom format options

    Available formats: canadian, modern, minimal
    """
    cv = await CVService.get_cv_by_id(cv_id, current_user["id"])

    # For now, we only support Canadian format
    # You can extend this to support multiple formats
    pdf_buffer = pdf_service.generate_canadian_cv_pdf(cv)

    filename = f"CV_{cv['full_name'].replace(' ', '_')}_{export_request.format}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
