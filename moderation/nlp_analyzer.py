import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import Dict, Any
from utils.logger import setup_logger
from utils.helpers import clean_text
from config import Config

# Download NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

logger = setup_logger(__name__)

class NLPAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.bad_words = self._load_bad_words()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text using NLP techniques."""
        cleaned_text = clean_text(text)
        
        # Sentiment analysis
        sentiment = self.sia.polarity_scores(cleaned_text)
        
        # Toxicity detection (simplified)
        toxicity_score = self._calculate_toxicity(cleaned_text)
        
        # Hate speech detection (simplified)
        hate_speech_score = self._detect_hate_speech(cleaned_text)
        
        # Explicit content detection
        explicit_score = self._detect_explicit_content(cleaned_text)
        
        result = {
            "flagged": (toxicity_score > Config.TOXICITY_THRESHOLD or 
                       hate_speech_score > Config.HATE_SPEECH_THRESHOLD or
                       explicit_score > Config.EXPLICIT_CONTENT_THRESHOLD),
            "scores": {
                "toxicity": toxicity_score,
                "hate_speech": hate_speech_score,
                "explicit_content": explicit_score,
                "sentiment_neg": sentiment["neg"],
                "sentiment_pos": sentiment["pos"],
                "sentiment_neu": sentiment["neu"],
                "sentiment_compound": sentiment["compound"]
            },
            "moderation_type": "nlp"
        }
        
        return result
    
    def _calculate_toxicity(self, text: str) -> float:
        """Calculate a toxicity score based on bad words and negative sentiment."""
        tokens = word_tokenize(text)
        bad_word_count = sum(1 for word in tokens if word.lower() in self.bad_words)
        
        # Normalize score between 0 and 1
        toxicity_score = min(bad_word_count / max(1, len(tokens)), 1.0)
        
        # Adjust with sentiment
        sentiment = self.sia.polarity_scores(text)
        toxicity_score = (toxicity_score * 0.7) + (sentiment["neg"] * 0.3)
        
        return toxicity_score
    
    def _detect_hate_speech(self, text: str) -> float:
        """Detect hate speech using keywords and sentiment."""
        hate_keywords = ['hate', 'kill', 'attack', 'race', 'religion', 'gender', 'sexist', 'racist']
        tokens = word_tokenize(text)
        
        hate_word_count = sum(1 for word in tokens if word.lower() in hate_keywords)
        hate_score = min(hate_word_count / max(1, len(tokens)) * 2, 1.0)  # More weight to hate words
        
        return hate_score
    
    def _detect_explicit_content(self, text: str) -> float:
        """Detect explicit content using keywords."""
        explicit_keywords = ['sex', 'sexual', 'nude', 'porn', 'fuck', 'ass', 'bitch']
        tokens = word_tokenize(text)
        
        explicit_word_count = sum(1 for word in tokens if word.lower() in explicit_keywords)
        explicit_score = min(explicit_word_count / max(1, len(tokens)), 1.0)
        
        return explicit_score
    
    def _load_bad_words(self) -> set:
        """Load a set of bad words for basic filtering."""
        # In a real application, you'd load this from a file or database
        common_bad_words = {
            'shit', 'fuck', 'asshole', 'bitch', 'bastard', 'damn', 'crap', 
            'dick', 'piss', 'slut', 'whore', 'fag', 'douche', 'cock', 'pussy'
        }
        return common_bad_words