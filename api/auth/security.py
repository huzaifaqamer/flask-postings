from passlib.context import CryptContext


def hash_password(password):
    crypt_context = CryptContext(schemes=['bcrypt_sha256'])
    return crypt_context.hash(password)


def verify_password(password, pwd_hash):
    crypt_context = CryptContext(schemes=['bcrypt_sha256'])
    return crypt_context.verify(password, pwd_hash)