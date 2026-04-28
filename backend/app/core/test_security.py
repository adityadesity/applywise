from app.core.security import (
    hash_password,
    verify_password
)

password = "mypassword123"

hashed = hash_password(password)

print("Hashed:", hashed)

is_valid = verify_password(
    password,
    hashed
)

print("Valid:", is_valid)