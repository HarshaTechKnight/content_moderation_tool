from .openai_moderator import OpenAIModerator
from .nlp_analyzer import NLPAnalyzer
from .content_filter import ContentFilter

class ContentModerator:
    def __init__(self):
        self.openai_moderator = OpenAIModerator()
        self.nlp_analyzer = NLPAnalyzer()
        self.content_filter = ContentFilter()
        
    def moderate(self, text: str) -> dict:
        """Run all moderation techniques on the text."""
        results = {
            "openai": self.openai_moderator.moderate(text),
            "nlp": self.nlp_analyzer.analyze(text),
            "rule_based": self.content_filter.filter(text)
        }
        
        # Combine results
        combined_result = self._combine_results(results, text)
        return combined_result
    
    def _combine_results(self, results: dict, text: str) -> dict:
        """Combine results from different moderation techniques."""
        # Implement your logic to combine results here
        # For now, we'll prioritize OpenAI results
        combined = results["openai"]
        combined["moderation_type"] = "combined"
        
        # Add explanations from other methods
        combined["additional_info"] = {
            "nlp_analysis": results["nlp"],
            "rule_based_flags": results["rule_based"]
        }
        
        # Final decision logic (can be more sophisticated)
        if combined["flagged"] or results["rule_based"]["flagged"]:
            combined["flagged"] = True
            
        return combined