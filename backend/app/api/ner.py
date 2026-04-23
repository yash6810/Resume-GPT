"""
API endpoint for Named Entity Recognition (NER) on resumes.
"""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.ner import get_ner_service

router = APIRouter()


class NERRequest(BaseModel):
    text: str
    extract_skills: bool = True
    extract_entities: bool = True


class NERResponse(BaseModel):
    entities: Dict[str, List[str]]
    skills: List[str]
    sections: Dict[str, str]


class TrainRequest(BaseModel):
    epochs: int = 30
    dropout: float = 0.5


@router.post("/ner/extract", response_model=NERResponse)
async def extract_entities(request: NERRequest):
    """
    Extract entities from resume text using NER.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        ner_service = get_ner_service()

        # Extract entities
        entities = {}
        if request.extract_entities:
            entities = ner_service.extract_entities(request.text)

        # Extract skills
        skills = []
        if request.extract_skills:
            skills = ner_service.extract_skills(request.text)

        # Extract sections
        sections = ner_service.extract_sections(request.text)

        return NERResponse(entities=entities, skills=skills, sections=sections)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error extracting entities: {str(e)}"
        )


@router.post("/ner/train")
async def train_ner_model(request: TrainRequest):
    """
    Train a custom NER model on resume data.
    This is an admin-only operation in production.
    """
    try:
        from app.services.train_ner import train_ner_model
        import os

        model_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "resume_ner"
        )

        # Run training in background (in production, use a task queue)
        train_ner_model(
            output_dir=model_path, n_iter=request.epochs, dropout=request.dropout
        )

        return {
            "status": "success",
            "message": f"Model trained for {request.epochs} epochs",
            "model_path": model_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model: {str(e)}")


@router.get("/ner/status")
async def ner_status():
    """
    Check NER service status and model information.
    """
    try:
        ner_service = get_ner_service()

        model_info = {
            "model_loaded": ner_service.nlp_base is not None
            or ner_service.nlp_custom is not None,
            "model_type": ner_service.model_type,
            "custom_model_exists": os.path.exists(ner_service.custom_model_path),
            "base_model_loaded": ner_service.nlp_base is not None,
            "custom_model_loaded": ner_service.nlp_custom is not None,
        }

        if ner_service.nlp_custom:
            model_info["pipeline"] = ner_service.nlp_custom.pipe_names
            model_info["entity_labels"] = list(
                ner_service.nlp_custom.pipe_labels.get("ner", [])
            )

        return model_info
    except Exception as e:
        return {"error": str(e), "model_loaded": False}
