import string
import random

def generateRandomAlphaNumericString(size=10):
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(size))

def generateRandomNumericString(size=10):
    chars = string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def generateRandomString(size=10):
    chars = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(size))