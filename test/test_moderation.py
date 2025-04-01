import unittest
from moderation import ContentModerator
from moderation.openai_moderator import OpenAIModerator
from moderation.nlp_analyzer import NLPAnalyzer
from moderation.content_filter import ContentFilter

class TestContentModeration(unittest.TestCase):
    def setUp(self):
        self.moderator = ContentModerator()
        self.openai_moderator = OpenAIModerator()
        self.nlp_analyzer = NLPAnalyzer()
        self.content_filter = ContentFilter()
    
    def test_clean_text(self):
        test_cases = [
            ("Hello http://example.com world!", "hello world"),
            ("This is a #test @user", "this is a test user"),
            ("Some! random? punctuation.", "some random punctuation")
        ]
        
        for input_text, expected in test_cases:
            cleaned = self.nlp_analyzer.clean_text(input_text)
            self.assertEqual(cleaned, expected)
    
    def test_content_filter(self):
        test_cases = [
            ("I hate all jews", True),  # Hate speech
            ("My credit card is 1234567812345678", True),  # Personal info
            ("Hello world", False)  # Clean
        ]
        
        for text, should_flag in test_cases:
            result = self.content_filter.filter(text)
            self.assertEqual(result["flagged"], should_flag)
    
    def test_nlp_analyzer(self):
        test_cases = [
            ("This is wonderful", {"flagged": False}),
            ("You're a stupid idiot", {"flagged": True})
        ]
        
        for text, expected in test_cases:
            result = self.nlp_analyzer.analyze(text)
            self.assertEqual(result["flagged"], expected["flagged"])
    
    # Note: OpenAI tests would require mocking the API calls

if __name__ == '__main__':
    unittest.main()