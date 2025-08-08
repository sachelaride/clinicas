from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from datetime import timedelta

def test_password_hashing():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

def test_create_and_decode_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_data = decode_access_token(token)
    assert decoded_data["sub"] == data["sub"]

def test_create_access_token_with_expiration():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=1)
    token = create_access_token(data, expires_delta=expires_delta)
    decoded_data = decode_access_token(token)
    assert decoded_data["sub"] == data["sub"]
    assert "exp" in decoded_data

def test_decode_invalid_token():
    invalid_token = "invalid.token.string"
    decoded_data = decode_access_token(invalid_token)
    assert decoded_data is None