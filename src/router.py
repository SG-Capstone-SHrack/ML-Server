from fastapi import APIRouter

from services.image import router as image_router
from inference import router as inference_router

# list of router
router = APIRouter()
router.include_router(image_router, tags=["image"])
router.include_router(inference_router, tags=["inference"])