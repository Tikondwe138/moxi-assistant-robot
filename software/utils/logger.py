import logging
import sys
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Provide consistent logging across MOXI modules, saving to both console and file.
    
    Args:
        name (str): The name of the logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Only configure if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Ensure logs directory exists
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "moxi.log")
        
        # Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        
        # File handler
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        
        logger.addHandler(ch)
        logger.addHandler(fh)
        
    return logger

def log_inventory_query(items: list, available_flags: list, success: bool):
    """
    Append an inventory query to the CSV file.
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    csv_file = os.path.join(log_dir, "inventory_queries.csv")
    
    # Create header if file doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            f.write("timestamp,items_queried,available,success\n")
            
    timestamp = datetime.now().isoformat()
    items_str = "|".join(items) if items else "None"
    avail_str = "|".join([str(val) for val in available_flags]) if available_flags else "None"
    
    with open(csv_file, 'a') as f:
        f.write(f"{timestamp},{items_str},{avail_str},{success}\n")

# Create a default system logger
sys_log = setup_logger("system")
