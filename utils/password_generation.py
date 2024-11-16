import random
import string

def generate_strong_password(length=12):
    """
    Generates a strong random password.

    Args:
        length (int): The desired length of the password. Default is 12.

    Returns:
        str: A randomly generated strong password.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+{}|:\"<>?"

    # Ensure at least one character from each category
    all_characters = lowercase + uppercase + digits + special
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special),
    ]

    # Fill the rest of the password length with random characters
    password += random.choices(all_characters, k=length - len(password))

    # Shuffle to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)
