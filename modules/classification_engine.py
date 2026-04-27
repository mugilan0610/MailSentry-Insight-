import logging

CATEGORIES = ["Sales Lead", "Support", "Invoice", "HR", "Internal", "Spam", "Manual Review"]

# Simple keyword weights for demonstration
KEYWORD_WEIGHTS = {
    "Sales Lead": {"buy": 3, "pricing": 2, "demo": 3, "interested": 2, "purchase": 3, "quote": 2, "sales": 3},
    "Support": {"help": 3, "issue": 3, "broken": 3, "error": 2, "bug": 2, "not working": 3, "support": 3},
    "Invoice": {"invoice": 4, "payment": 3, "billing": 3, "receipt": 2, "charge": 2, "due": 2},
    "HR": {"interview": 3, "resume": 3, "application": 2, "hiring": 2, "leave": 2, "job": 2},
    "Internal": {"meeting": 2, "all hands": 3, "townhall": 3, "project": 1, "update": 1, "team": 1},
    "Spam": {"unsubscribe": 3, "lottery": 4, "winner": 4, "free money": 4, "click here": 2, "viagra": 5}
}

def classify_email(text: str) -> tuple:
    """
    Classifies an email based on highest aggregate keyword score.
    Returns (Category: str, Confidence: int)
    """
    try:
        if not text:
            return ("Manual Review", 0)
            
        scores = {cat: 0 for cat in CATEGORIES if cat != "Manual Review"}
        
        # Calculate scores
        for category, keywords in KEYWORD_WEIGHTS.items():
            for keyword, weight in keywords.items():
                if keyword in text:
                    count = text.count(keyword)
                    scores[category] += (weight * count)
                    
        # Find highest score
        best_category = max(scores, key=scores.get)
        max_score = scores[best_category]
        
        # Calculate confidence (assuming a score of 10 is 100% confidence for this demo logic)
        confidence = min(int((max_score / 10.0) * 100), 100)
        
        if max_score == 0:
            return ("Manual Review", 0)
        elif confidence < 30:
            return ("Manual Review", confidence) # Flag low confidence
        else:
            return (best_category, confidence)
            
    except Exception as e:
        logging.error(f"Error in classification: {e}")
        return ("Manual Review", 0)
