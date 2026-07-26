import random
import string

from e_commerce.models import User


def generate_referral_code( length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not User.objects.filter(referral_code=code).exists():
            return code