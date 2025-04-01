import openai
from typing import Dict, Any
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class OpenAIModerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.categories = {
            "hate": "Content that expresses hate or promotes violence against people",
            "hate/threatening": "Hateful content that includes violence or serious harm",
            "self-harm": "Content that promotes self-harm",
            "sexual": "Sexually explicit content",
            "sexual/minors": "Sexual content involving minors",
            "violence": "Violent content",
            "violence/graphic": "Extremely violent or graphic content"
        }
    
    def moderate(self, text: str) -> Dict[str, Any]:
        """Moderate content using OpenAI's moderation API."""
        try:
            response = openai.Moderation.create(input=text)
            result = response["results"][0]
            
            moderation_result = {
                "flagged": result["flagged"],
                "categories": {cat: result["categories"][cat] for cat in self.categories},
                "scores": {cat: result["category_scores"][cat] for cat in self.categories},
                "moderation_type": "openai"
            }
            
            # Add explanation if flagged
            if moderation_result["flagged"]:
                moderation_result["explanation"] = self._generate_explanation(text, moderation_result)
            
            return moderation_result
            
        except Exception as e:
            logger.error(f"OpenAI moderation failed: {str(e)}")
            return {
                "flagged": False,
                "categories": {cat: False for cat in self.categories},
                "scores": {cat: 0.0 for cat in self.categories},
                "moderation_type": "openai",
                "error": str(e)
            }
    
    def _generate_explanation(self, text: str, result: Dict[str, Any]) -> str:
        """Generate an explanation for why content was flagged."""
        flagged_categories = [cat for cat, flagged in result["categories"].items() if flagged]
        
        prompt = f"""
        The following text was flagged by the moderation system for these categories: {', '.join(flagged_categories)}.
        Text: "{text}"
        
        Please provide a detailed explanation of why this text violates content policies for each flagged category.
        Be specific about the problematic phrases or words and how they relate to each category.
        """
        
        try:
            chat_response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a content moderation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.OPENAI_TEMPERATURE
            )
            return chat_response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to generate explanation: {str(e)}")
            return "Content was flagged but explanation could not be generated."