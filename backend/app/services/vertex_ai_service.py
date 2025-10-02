from typing import Optional, Dict, Any
import json
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
from app.core.config import settings


class VertexAIService:
    """Service for interacting with Google Vertex AI"""

    def __init__(self):
        if settings.GCP_PROJECT_ID:
            aiplatform.init(
                project=settings.GCP_PROJECT_ID,
                location=settings.GCP_LOCATION
            )
            self.model = GenerativeModel(settings.VERTEX_AI_MODEL)
        else:
            self.model = None

    async def generate_cv_content(
        self,
        industry_name: str,
        job_title: str,
        experience: list,
        education: list,
        skills: list,
        summary: Optional[str] = None,
        certifications: Optional[list] = None,
        languages: Optional[list] = None,
        tips: Optional[list] = None
    ) -> Dict[str, Any]:
        """Generate optimized CV content using Vertex AI"""

        if not self.model:
            # Fallback if Vertex AI not configured
            return self._generate_fallback_content(
                industry_name, job_title, experience, education, skills, summary
            )

        # Build the prompt
        prompt = self._build_cv_prompt(
            industry_name, job_title, experience, education,
            skills, summary, certifications, languages, tips
        )

        try:
            generation_config = GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Parse the response
            result = self._parse_ai_response(response.text)
            return result

        except Exception as e:
            print(f"Vertex AI Error: {str(e)}")
            # Fallback to basic content
            return self._generate_fallback_content(
                industry_name, job_title, experience, education, skills, summary
            )

    def _build_cv_prompt(
        self,
        industry: str,
        job_title: str,
        experience: list,
        education: list,
        skills: list,
        summary: Optional[str],
        certifications: Optional[list],
        languages: Optional[list],
        tips: Optional[list]
    ) -> str:
        """Build the AI prompt for CV generation"""

        prompt = f"""You are an expert Canadian resume writer specializing in the {industry} industry.

Task: Optimize the following resume content for a {job_title} position in Canada. Follow Canadian resume standards:
- No photo, age, or marital status
- Focus on achievements with metrics
- Use action verbs
- Optimize for ATS (Applicant Tracking Systems)
- Keep it concise (1-2 pages)

INPUT DATA:

Job Title: {job_title}
Industry: {industry}

"""

        if summary:
            prompt += f"Current Summary:\n{summary}\n\n"

        prompt += f"Work Experience:\n"
        for exp in experience:
            prompt += f"- {exp.get('position')} at {exp.get('company')} ({exp.get('start_date')} - {exp.get('end_date', 'Present')})\n"
            for resp in exp.get('responsibilities', []):
                prompt += f"  • {resp}\n"

        prompt += f"\nEducation:\n"
        for edu in education:
            prompt += f"- {edu.get('degree')} in {edu.get('field_of_study')} from {edu.get('institution')} ({edu.get('graduation_date')})\n"

        prompt += f"\nSkills:\n{', '.join(skills)}\n"

        if certifications:
            prompt += f"\nCertifications:\n"
            for cert in certifications:
                prompt += f"- {cert.get('name')} from {cert.get('issuing_organization')}\n"

        if languages:
            prompt += f"\nLanguages:\n"
            for lang in languages:
                prompt += f"- {lang.get('language')}: {lang.get('proficiency')}\n"

        if tips:
            prompt += f"\nIndustry-Specific Tips:\n"
            for tip in tips:
                prompt += f"- {tip}\n"

        prompt += """

OUTPUT (respond ONLY with valid JSON):
{
  "optimized_summary": "A compelling 3-4 sentence professional summary optimized for this role",
  "optimized_skills": ["skill1", "skill2", ...],  // Reordered by relevance, include keywords
  "key_achievements": ["achievement1", "achievement2", ...],  // Top 5 quantified achievements
  "ats_keywords": ["keyword1", "keyword2", ...],  // Important keywords for ATS
  "tips": ["tip1", "tip2", ...],  // 3-5 specific tips for this application
  "ats_score": 85  // Estimated ATS compatibility score (0-100)
}
"""

        return prompt

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response to extract structured data"""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return result
            else:
                raise ValueError("No JSON found in response")

        except Exception as e:
            print(f"Error parsing AI response: {str(e)}")
            # Return basic structure
            return {
                "optimized_summary": "Experienced professional seeking new opportunities.",
                "optimized_skills": [],
                "key_achievements": [],
                "ats_keywords": [],
                "tips": ["Tailor your resume for each application"],
                "ats_score": 70
            }

    def _generate_fallback_content(
        self,
        industry: str,
        job_title: str,
        experience: list,
        education: list,
        skills: list,
        summary: Optional[str]
    ) -> Dict[str, Any]:
        """Generate basic content when AI is not available"""

        # Extract key info
        years_exp = len(experience)
        top_skills = skills[:10] if len(skills) > 10 else skills

        fallback_summary = summary or f"Experienced {job_title} with {years_exp}+ years in the {industry} industry."

        return {
            "optimized_summary": fallback_summary,
            "optimized_skills": top_skills,
            "key_achievements": [
                "Demonstrated expertise in core responsibilities",
                "Contributed to team and organizational success",
                "Maintained professional development"
            ],
            "ats_keywords": top_skills[:5],
            "tips": [
                "Quantify your achievements with specific metrics",
                "Use action verbs to describe your responsibilities",
                f"Highlight {industry}-specific skills and certifications",
                "Tailor your resume for each application"
            ],
            "ats_score": 75
        }


# Singleton instance
vertex_ai_service = VertexAIService()
