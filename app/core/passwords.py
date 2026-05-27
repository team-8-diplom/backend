from passlib.context import CryptContext
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
legacy_password_hash = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception:
        return legacy_password_hash.verify(plain_password, hashed_password)
