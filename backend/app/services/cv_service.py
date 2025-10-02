from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.models.cv import industries, user_cvs, cv_generation_history
from app.schemas.cv import (
    IndustryCreate, CVGenerateInput, UserCVCreate,
    CVGenerateResponse
)
from app.services.vertex_ai_service import vertex_ai_service
from app.db.database import database
import json


class IndustryService:
    """Service for managing industries"""

    @staticmethod
    async def create_industry(industry_data: IndustryCreate) -> dict:
        """Create a new industry"""
        existing = await database.fetch_one(
            industries.select().where(industries.c.name == industry_data.name)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Industry already exists"
            )

        query = industries.insert().values(
            name=industry_data.name,
            name_fr=industry_data.name_fr,
            description=industry_data.description,
            tips=industry_data.tips,
            keywords=industry_data.keywords
        )
        industry_id = await database.execute(query)
        return await IndustryService.get_industry_by_id(industry_id)

    @staticmethod
    async def get_industry_by_id(industry_id: int) -> Optional[dict]:
        """Get industry by ID"""
        query = industries.select().where(industries.c.id == industry_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all_industries() -> List[dict]:
        """Get all active industries"""
        query = industries.select().where(industries.c.is_active == True)
        return await database.fetch_all(query)


class CVService:
    """Service for CV generation and management"""

    @staticmethod
    async def generate_cv(user_id: int, cv_input: CVGenerateInput) -> CVGenerateResponse:
        """Generate a CV using Vertex AI"""

        # Get industry info
        industry = await IndustryService.get_industry_by_id(cv_input.industry_id)
        if not industry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Industry not found"
            )

        # Create generation history entry
        history_query = cv_generation_history.insert().values(
            user_id=user_id,
            industry_id=cv_input.industry_id,
            prompt=f"Generate CV for {cv_input.job_title} in {industry['name']}",
            status="pending"
        )
        history_id = await database.execute(history_query)

        try:
            # Convert Pydantic models to dicts
            experience_dicts = [exp.dict() for exp in cv_input.experience]
            education_dicts = [edu.dict() for edu in cv_input.education]
            cert_dicts = [cert.dict() for cert in cv_input.certifications] if cv_input.certifications else None
            lang_dicts = [lang.dict() for lang in cv_input.languages] if cv_input.languages else None

            # Generate optimized content using Vertex AI
            ai_result = await vertex_ai_service.generate_cv_content(
                industry_name=industry['name'],
                job_title=cv_input.job_title,
                experience=experience_dicts,
                education=education_dicts,
                skills=cv_input.skills,
                summary=cv_input.summary,
                certifications=cert_dicts,
                languages=lang_dicts,
                tips=industry.get('tips')
            )

            # Build complete CV content
            cv_content = {
                "original_input": cv_input.dict(),
                "ai_optimizations": ai_result,
                "industry": {
                    "id": industry['id'],
                    "name": industry['name']
                }
            }

            # Create user CV record
            cv_data = UserCVCreate(
                title=f"{cv_input.job_title} - {industry['name']}",
                full_name=cv_input.full_name,
                email=cv_input.email,
                phone=cv_input.phone,
                location=cv_input.location,
                summary=ai_result.get('optimized_summary', cv_input.summary),
                experience=experience_dicts,
                education=education_dicts,
                skills=ai_result.get('optimized_skills', cv_input.skills),
                certifications=cert_dicts,
                languages=lang_dicts,
                format_type="canadian",
                industry_id=cv_input.industry_id,
                cv_content=cv_content
            )

            cv_query = user_cvs.insert().values(
                user_id=user_id,
                **cv_data.dict()
            )
            cv_id = await database.execute(cv_query)

            # Update generation history
            await database.execute(
                cv_generation_history.update()
                .where(cv_generation_history.c.id == history_id)
                .values(
                    cv_id=cv_id,
                    status="completed",
                    generated_content=ai_result
                )
            )

            # Return response
            return CVGenerateResponse(
                cv_id=cv_id,
                optimized_summary=ai_result.get('optimized_summary', ''),
                optimized_skills=ai_result.get('optimized_skills', []),
                tips=ai_result.get('tips', []),
                ats_score=ai_result.get('ats_score', 75),
                suggestions=ai_result.get('key_achievements', [])
            )

        except Exception as e:
            # Update history with error
            await database.execute(
                cv_generation_history.update()
                .where(cv_generation_history.c.id == history_id)
                .values(status="failed", error_message=str(e))
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"CV generation failed: {str(e)}"
            )

    @staticmethod
    async def get_user_cvs(user_id: int) -> List[dict]:
        """Get all CVs for a user"""
        query = user_cvs.select().where(user_cvs.c.user_id == user_id).order_by(user_cvs.c.created_at.desc())
        return await database.fetch_all(query)

    @staticmethod
    async def get_cv_by_id(cv_id: int, user_id: int) -> Optional[dict]:
        """Get a specific CV"""
        query = user_cvs.select().where(
            (user_cvs.c.id == cv_id) & (user_cvs.c.user_id == user_id)
        )
        cv = await database.fetch_one(query)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found"
            )
        return cv

    @staticmethod
    async def delete_cv(cv_id: int, user_id: int) -> bool:
        """Delete a CV"""
        cv = await CVService.get_cv_by_id(cv_id, user_id)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found"
            )

        query = user_cvs.delete().where(user_cvs.c.id == cv_id)
        await database.execute(query)
        return True

    @staticmethod
    async def toggle_favorite(cv_id: int, user_id: int) -> dict:
        """Toggle favorite status of a CV"""
        cv = await CVService.get_cv_by_id(cv_id, user_id)

        new_favorite_status = not cv['is_favorite']
        query = user_cvs.update().where(user_cvs.c.id == cv_id).values(is_favorite=new_favorite_status)
        await database.execute(query)

        return await CVService.get_cv_by_id(cv_id, user_id)
