from fastapi import APIRouter
from .llm import v1_router as llm_v1_router


v1_router = APIRouter(prefix="/external", tags=["external"])
v1_router.include_router(llm_v1_router)
