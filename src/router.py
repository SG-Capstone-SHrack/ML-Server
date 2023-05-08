from fastapi import APIRouter

from services.image import router as image_router

# list of router
router = APIRouter()
router.include_router(image_router, tags=["image"])
