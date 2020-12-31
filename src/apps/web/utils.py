import hashlib

from django.conf import settings


def generate_user_auth_hash(user_id: int, user_name: str) -> str:
    user_hash = f'{user_id}{settings.SECRET_KEY}{user_name}'
    sha_signature = encrypt_string(user_hash)
    return sha_signature


def encrypt_string(string: str) -> str:
    sha_signature = hashlib.sha256(string.encode()).hexdigest()
    return sha_signature
