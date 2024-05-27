import re


def validator_password(password):
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', password):
        return False
    return True