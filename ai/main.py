from ai.core.config import get_settings
settings = get_settings()

from ai.service.compare_image_service import CompareImageService

from typing import Optional, List
from fastapi import FastAPI, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse



# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


def get_compare_image_service():
    return CompareImageService()

@app.post("/compare")
async def compare_image(
    images: List[UploadFile],
    user_input: Optional[str] = None,
    service: CompareImageService = Depends(get_compare_image_service)
):
    return await service.compare(user_input=user_input, images=images)
