import random


def generate_random_key(size, alpha_numeric=False):
    letters = "1234567890"
    if alpha_numeric:
        letters += "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    random_key = ""
    for _ in range(size):
        random_key += random.choice(letters)
    return random_key
