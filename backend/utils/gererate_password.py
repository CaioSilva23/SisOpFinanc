import random
import string


def generate_temp_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))
