import re
import logging

def preprocess_text(text: str) -> str:
    """
    Cleans email text by stripping HTML, normalizing to lowercase,
    and compressing whitespace.
    """
    try:
        if not text:
            return ""
        
        # Strip HTML/CSS tags using regex
        text = re.sub(r'<style.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Lowercase normalization
        text = text.lower()
        
        # Whitespace compression
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except Exception as e:
        # NFR2: Silently handle exceptions
        logging.error(f"Error in preprocessing: {e}")
        return ""
