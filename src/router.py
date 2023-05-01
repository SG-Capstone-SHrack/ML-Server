from fastapi import APIRouter

from services.image import router as image_router
from streamlit import router as streamlit_router

# list of router
router = APIRouter()
router.include_router(image_router, tags=["image"])
router.include_router(streamlit_router, tags=["streamlit"])
