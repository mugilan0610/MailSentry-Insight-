import re
import logging

def extract_entities(text: str) -> dict:
    """
    Extracts specific entities from text using regex.
    Targets: Phone Numbers, Email Addresses, INV-XXXX, TCK-XXXX, Currency values
    """
    entities = {
        "phone_numbers": [],
        "email_addresses": [],
        "invoices": [],
        "tickets": [],
        "currency_values": []
    }
    
    try:
        if not text:
            return entities
            
        # Email Addresses
        entities["email_addresses"] = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
        
        # Phone Numbers (basic pattern)
        entities["phone_numbers"] = list(set(re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)))
        
        # INV-XXXX
        entities["invoices"] = list(set(re.findall(r'\binv-\d+\b', text, flags=re.IGNORECASE)))
        
        # TCK-XXXX
        entities["tickets"] = list(set(re.findall(r'\btck-\d+\b', text, flags=re.IGNORECASE)))
        
        # Currency values (e.g., $100, $100.00, £50)
        entities["currency_values"] = list(set(re.findall(r'[$£€¥]\s*\d+(?:[.,]\d{1,2})?', text)))
        
    except Exception as e:
        logging.error(f"Error in extraction: {e}")
        
    return entities
