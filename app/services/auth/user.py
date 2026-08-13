def check_existing_user(email: str) -> bool:
    """
    Check if a user with the given email already exists in the database.
    # call the function from repository layer to check if the user exists in the db
    
    Args:
        email (str): The email address to check.
    
    Returns:
        bool: True if the user exists, False otherwise.
    """
    # for now for testing -> we return true
    return False
    