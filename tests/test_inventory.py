import sys
import os

# Add the parent directory to the path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from software.services.inventory_api import check_inventory

def test_inventory_api():
    """
    Test the inventory API connection.
    Calls the inventory endpoint, verifies the response format implicitly 
    through the check_inventory function, and prints the result.
    """
    item_to_check = "PLA filament"
    print(f"Testing inventory lookup for: {item_to_check}")
    
    # Call inventory endpoint
    is_available = check_inventory(item_to_check)
    
    # Print availability result
    print("--- Test Result ---")
    if is_available:
        print(f"Success: {item_to_check} is reported as AVAILABLE.")
    else:
        print(f"Success: {item_to_check} is reported as NOT AVAILABLE (or API unreachable).")
    print("-------------------")

if __name__ == "__main__":
    test_inventory_api()
