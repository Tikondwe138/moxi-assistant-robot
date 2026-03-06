# Contacts directory linking names to roles and phone numbers
CONTACTS_DIRECTORY = {
    "nelson": {
        "role": "design technician",
        "phone": "555-0100"
    },
    "alice": {
        "role": "studio manager",
        "phone": "555-0101"
    },
    "bob": {
        "role": "lead designer",
        "phone": "555-0102"
    }
}

def get_contact(name: str) -> str:
    """
    Retrieve design studio contact information by name.
    
    Args:
        name (str): The name of the person to look up.
        
    Returns:
        str: The phone number if found, or an error message otherwise.
    """
    name_lower = name.lower()
    
    if name_lower in CONTACTS_DIRECTORY:
        return CONTACTS_DIRECTORY[name_lower]["phone"]
    else:
        return f"Error: Contact '{name}' not found."
