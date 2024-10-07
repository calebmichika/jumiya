import re
def checkpaswordvalidity(password):
    if len(password) < 6:
        return "Your password is too short"
    elif re.search(r"[A-Z]", password):
        return "Atleast 1 upper case"
    elif re.search(r"[a-z]", password):
        return "Atleast 1 lower case"
    elif re.search(r"[0-9]", password):
        return "Atleast 1 digit"
    elif re.search(r"[~!@#$%^&*]", password):
        return "Atleast 1 special character"
    else:
        return true
    