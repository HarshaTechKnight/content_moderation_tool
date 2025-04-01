import re
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ContentFilter:
    def __init__(self):
        self.patterns = self._load_patterns()
    
    def filter(self, text: str) -> Dict[str, Any]:
        """Apply rule-based content filtering."""
        results = {
            "flagged": False,
            "matched_rules": [],
            "moderation_type": "rule_based"
        }
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    results["flagged"] = True
                    results["matched_rules"].append({
                        "category": category,
                        "pattern": pattern
                    })
        
        return results
    
    def _load_patterns(self) -> dict:
        """Load regular expression patterns for content filtering."""
        return {
            "hate_speech": [
                r'\b(kill|attack|exterminate)\s+(all|the)?\s*(blacks|jews|muslims|gays)\b',
                r'\b(white|aryan)\s+(power|supremacy)\b',
                r'\b(women|girls)\s+(belong|should)\s+(in|to)\s+the\s+(kitchen|home)\b'
            ],
            "threats": [
                r'\b(i\'ll|i will|im gonna|going to)\s+(kill|murder|attack|beat)\s+(you|him|her|them)\b',
                r'\b(you|they)\s+(should|deserve to)\s+(die|burn in hell)\b'
            ],
            "personal_info": [
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
                r'\b\d{16}\b',  # Credit card number
                r'\b\d{3}\s\d{3}\s\d{4}\b'  # Phone number
            ],
            "explicit_content": [
                r'\b(sex|sexual|nude|porn)\b',
                r'\b(fuck|ass|bitch|cock|pussy)\b'
            ]
        }