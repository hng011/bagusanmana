from ai.core.config import get_settings
settings = get_settings()

from typing import Optional 
from google import genai
from google.genai import types

# from ai.pembungkus_ai.secret_system_prompts.image_comparator_system_prompt import system_prompt 

class ImageComparator:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )
        
    
    def call(self, user_input: Optional[str], images: list[bytes]) -> dict:
        try:
            #TODO: ADD RETURN COMPARISON RESULT
            _response = self.client.models.generate_content(
                model=settings.MODEL_ID,
                contents=self.setup_contents(user_input, images),
                config=self._generate_content_config,
            )
        except Exception as e:
            #TODO: LOG GET ERROR
            raise Exception(f"Unable to compare -> {e}")
        
        if isinstance(_response, dict):
            # TODO: LOG GET ERROR
            raise ValueError(f"Unexpected Output: Expected the output in JSON format but got {_response}")
        
        #TODO: LOG RESPONSE SENT TO SERVICE
        return _response.parsed
        
        
    def setup_contents(self, user_input: Optional[str], images: list[bytes]) -> list:
        
        # TODO: LOG ABOUT CONTENT SETUP
        
        user_prompt_template = """
        <Task>
        Compare the given image and choose the best one
        <Task>
        """
        
        if user_input:
            user_prompt_template += f"""
            <Context>
            {user_input}
            </Context>
            """
        
        
        try:            
            parts = [types.Part.from_bytes(data=i, mime_type="image/jpeg") for i in images]
            user_prompt = types.Part.from_text(text=user_prompt_template)
            parts.append(user_prompt)
            
            return [
                types.Content(
                    role="user",
                    parts=parts
                ),
            ]
            
        except Exception as e:
            raise Exception(f"Error while setup the content -> {e}")
        
        
    @property
    def _generate_content_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            temperature=settings.TEMPERATURE,
            top_p=settings.TOP_P,
            max_output_tokens=settings.OUTPUT_LENGTH,
            system_instruction=settings.IMAGE_COMPARATOR_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_json_schema=self._response_json_schema,
        )
        
        
    @property
    def _response_json_schema(self) -> dict:
        return {
            "type": "object",
            "required": [
                "winner_index",
                "scores",
                "winner_reason",
                "loser_reason",
                "tip",
            ],
            "properties": {
                "winner_index": {
                    "type": "integer",
                    "description": "the winner image's index starting from 0",
                },
                "scores": {
                    "type": "array",
                    "description": "list of images' score in integer",
                },
                "winner_reason": {
                    "type": "string",
                    "description": "the reason of why the image's winner is better than another",
                },
                "loser_reason": {
                    "type": "string",
                    "description": "the critique of the losers",
                },
                "tip": {
                    "type": "string",
                    "description": "a tip to improve the winner image",
                }
            }
        }
    