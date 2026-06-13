from hashlib import sha256

def hash_password(password):
    return sha256(
        password.encode()
    ).hexdigest()

def verify_password(
    plain_password,
    hashed_password,
):
    return (
        sha256(
            plain_password.encode()
        ).hexdigest()
        == hashed_password
    )