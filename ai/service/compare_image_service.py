from ai.pembungkus_ai.ai_image_comparator import ImageComparator
from ai.core.config import get_settings
settings = get_settings()

from typing import List
from fastapi import UploadFile
from PIL import Image
from io import BytesIO


class CompareImageService:
    def __init__(self):
        self._image_comparator = ImageComparator()

    
    async def compare(self, user_input: str, images: List[UploadFile]) -> dict:
        #TODO: ADD LOG START COMPARING IMAGE
        try:
            return self._image_comparator.call(
                user_input=user_input,
                images=await self._process_images(images)
            )
        except Exception as e:
            #TODO: ADD ERROR LOG
            raise Exception(f"Error while comparing images -> {e}") 
        

    async def _process_images(self, images: List[UploadFile]) -> list[bytes]:
        #TODO: ADD LOG PROCESS IMAGE
        processed_images = []
        
        if len(images) < 2:
            raise ValueError("Minimum 2 images")
        
        try:
            for img in images:
                content = await img.read()
                raw_bytes = Image.open(BytesIO(content))
                
                if raw_bytes.format not in ["JPEG", "JPG"]:
                    if raw_bytes.mode in ("RGBA", "LA", "P"):
                        raw_bytes = raw_bytes.convert("RGB")
                
                    output = BytesIO()
                    raw_bytes.save(output, format="JPEG")
                    raw_bytes = output.getvalue()
                else:
                    raw_bytes = content

                processed_images.append(raw_bytes)
            
            return processed_images
                                
        except Exception as e:
            #TODO: ADD ERROR LOG
            raise Exception(f"Error while processing image -> {e} ")
