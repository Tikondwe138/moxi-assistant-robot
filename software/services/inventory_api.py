import requests
import sys
import os
import time

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    from utils.logger import setup_logger, log_inventory_query
except ImportError:
    config = None
    log_inventory_query = lambda x, y, z: None

logger = setup_logger("inventory_api") if 'setup_logger' in globals() else None

def check_inventory_batch(items: list[str], max_retries: int = 3) -> dict:
    """
    Query the design studio website inventory for multiple items with retry logic.
    
    Args:
        items: List of item names.
        max_retries: How many times to retry on API failure.
        
    Returns:
        dict: Mapping of item name to boolean availability.
    """
    if not config or not hasattr(config, 'INVENTORY_API'):
        if logger: logger.error("INVENTORY_API not configured.")
        return {item: False for item in items}
        
    results = {}
    success = False
    
    for item in items:
        item_success = False
        for attempt in range(max_retries):
            try:
                if logger: logger.debug(f"Querying '{item}' (Attempt {attempt+1}/{max_retries})")
                response = requests.get(config.INVENTORY_API, params={"item": item}, timeout=5)
                response.raise_for_status()
                
                data = response.json()
                is_available = data.get("available", False)
                results[item] = is_available
                item_success = True
                success = True # At least one succeeded
                break # Break out of retry loop for this item
                
            except requests.exceptions.RequestException as e:
                if logger: logger.warning(f"Inventory API error on '{item}': {e}")
                time.sleep(1) # Backoff
            except ValueError:
                if logger: logger.error("Invalid JSON response from inventory API")
                break # Non-recoverable parsing error
                
        if not item_success:
            results[item] = False
            
    # Log the multi-query to CSV
    log_inventory_query(items, list(results.values()), success)
        
    return results

def check_inventory(item: str) -> bool:
    """Backward compatible wrapper for single item queries."""
    results = check_inventory_batch([item])
    return results.get(item, False)
