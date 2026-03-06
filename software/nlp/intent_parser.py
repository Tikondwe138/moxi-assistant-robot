import sys
import os
import spacy

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Load the small English language model
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spacy model 'en_core_web_sm' not found. Fallback mode active.")
    nlp = None

def parse_intent(text: str) -> dict:
    """
    Use spaCy to classify intent and extract entities (like items or names).
    
    Args:
        text (str): The recognized speech text.
        
    Returns:
        dict: Containing 'intent' and 'entities'.
    """
    text = text.lower()
    
    result = {
        "intent": "unknown",
        "entities": []
    }
    
    # Fallback/Basic Regex intent matching if spaCy isn't loaded or for speed
    if any(greet in text for greet in ["hello", "hi", "hey"]):
        result["intent"] = "greeting"
        
    elif "looking for" in text or "contact" in text or "call" in text:
        result["intent"] = "contact_lookup"
        # Extract name using spaCy if available
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    result["entities"].append(ent.text)
        # Fallback simple extraction
        if not result["entities"] and "looking for" in text:
            parts = text.split("looking for")
            if len(parts) > 1:
                name_part = parts[1].strip()
                result["entities"].append(name_part.split()[0] if name_part else "")
                
    elif "available" in text or "inventory" in text or "stock" in text:
        result["intent"] = "inventory_check"
        # Naive extraction for "Is [item1] and [item2] available"
        item_text = text.replace("are", "").replace("is", "").replace("available", "").replace("in stock", "").strip()
        # Clean up filler words
        for word in ["the", "any", "some", "check", "if"]:
            item_text = item_text.replace(f" {word} ", " ")
            if item_text.startswith(f"{word} "):
                item_text = item_text[len(word)+1:]
                
        # Split by "and" to handle batch queries
        items = [i.strip() for i in item_text.split(" and ") if i.strip()]
        if items:
            result["entities"].extend(items)
        else:
            result["entities"].append(item_text)
            
    elif "wave" in text or "gesture" in text:
        result["intent"] = "gesture_command"
        result["entities"].append("wave") # Default to wave for text command
        
    elif any(q in text for q in ["exit", "quit", "stop", "shutdown"]):
        result["intent"] = "exit"
        
    return result
