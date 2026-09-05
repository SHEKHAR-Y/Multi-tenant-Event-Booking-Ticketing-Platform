import pytest
import uuid

from app.core.security import create_refresh_token, decode_refresh_token, create_access_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError

from datetime import timedelta

def test_create_refresh_token():
    mock_user_id = uuid.uuid4() # used as the subject encoded in the token 

    subject = str(mock_user_id) 
    assert create_refresh_token(subject=subject)

def test_decode_refresh_token():
    mock_user_id = uuid.uuid4() # used as the subject encoded in the token 
    
    subject = str(mock_user_id) 
    test_token, test_jti, test_expiry = create_refresh_token(subject=subject)
    payload = decode_refresh_token(test_token) 
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"

def test_decode_refresh_token_tampered_token():
    mock_user_id = uuid.uuid4() # used as the subject encoded in the token 
    
    subject = str(mock_user_id) 
    test_token, test_jti, test_expiry = create_refresh_token(subject=subject)
    # Modify the token to simulate tampering
    test_token = test_token[:-1] + "invalid"
    with pytest.raises(InvalidTokenError):
        decode_refresh_token(test_token)

def test_decode_refresh_token_expired_token():
    mock_user_id = uuid.uuid4() # used as the subject encoded in the token 
    
    subject = str(mock_user_id) 
    test_token, test_jti, test_expiry = create_refresh_token(subject=subject, expires_delta=timedelta(-1))  # Set expiration in the past
    with pytest.raises(TokenExpiredError):
        decode_refresh_token(test_token)

def test_decode_wrong_token_type():
    mock_user_id = uuid.uuid4() # used as the subject encoded in the token

    subject = str(mock_user_id)
    test_token = create_access_token(subject=subject)  # Create an access token instead of a refresh token

    # Decode the token and check the payload for the wrong token type
    with pytest.raises(InvalidTokenError): 
        decode_refresh_token(test_token)