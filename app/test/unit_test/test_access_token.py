import pytest

import uuid

from datetime import timedelta

from app.core.security import create_access_token, decode_access_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError


def test_access_token_tampered_token():
    # create token 
    # create a random uuid to pass as subject in create_access_token 
    mock_user_id = uuid.uuid4()

    test_token = create_access_token(subject=str(mock_user_id))

    # tamper token 
    tampered_token = test_token[:-5] + "aaaaa"

    with pytest.raises(InvalidTokenError):
        decode_access_token(tampered_token)

def test_access_token_expried():
    # create token 
    # create a random uuid to pass as subject in create_access_token 
    mock_user_id = uuid.uuid4()

    test_token = create_access_token(subject=str(mock_user_id), expires_delta=timedelta(-1))


    with pytest.raises(TokenExpiredError):
        decode_access_token(test_token)

def test_access_token_success():
    # create token 
    # create a random uuid to pass as subject in create_access_token 
    mock_user_id = uuid.uuid4()

    test_token = create_access_token(subject=str(mock_user_id), expires_delta=timedelta(15))
    assert decode_access_token(test_token)