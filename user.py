import re

def is_valid_name(name):
    # At least 3 letters, only letters
    return bool(re.fullmatch(r"[a-zA-Z]{3,}", name))

def is_valid_email(email):
    # Simple email regex
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))

def is_valid_password(password, firstname="", lastname=""):
    # At least 8, max 40, at least one letter, one number, one special char (unless >=14), no first/last name, at least 6 unique chars
    if not (8 <= len(password) <= 40):
        return False, "Password must be between 8 and 40 characters"
    if not re.search(r"[a-zA-Z]", password):
        return False, "Password must contain at least one letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if len(password) < 14 and not re.search(r"[^a-zA-Z0-9]", password):
        return False, "Password must contain at least one special character"
    if firstname and firstname.lower() in password.lower():
        return False, "Password must not contain your first name"
    if lastname and lastname.lower() in password.lower():
        return False, "Password must not contain your last name"
    if len(set(password)) < 6:
        return False, "Password must contain at least 6 unique characters"
    return True, ""

def validate_registration(data):
    # data: dict with keys 'firstname', 'lastname', 'email', 'password'
    firstname = data.get("firstname", "")
    lastname = data.get("lastname", "")
    email = data.get("email", "")
    password = data.get("password", "")

    if not is_valid_email(email):
        return False, "Invalid email format."
    if not is_valid_name(firstname):
        return False, "Invalid first name."
    if not is_valid_name(lastname):
        return False, "Invalid last name."
    valid_pwd, pwd_msg = is_valid_password(password, firstname, lastname)
    if not valid_pwd:
        return False, pwd_msg
    return True, None
