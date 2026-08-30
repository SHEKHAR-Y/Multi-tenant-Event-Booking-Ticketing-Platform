import pytest

def test_register_invalid_email(test_client):
    payload = {
            "email": "test.com", # pydantic verify email by checking '@' in it 
            "username": "test_username",
            "password": "anyvalidpassword"  
        }

    response = test_client.post("/api/v1/register", json=payload)
    assert response.status_code == 422


def test_register_invalid_password(test_client):
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "invalid" # the password length must me >= 8 and <= 64 therefore use len("invalid") = 7 
        }

    response = test_client.post("/api/v1/register", json=payload)
    assert response.status_code == 422

def test_register_username_too_short(test_client):
    payload = {
            "email": "test@test.com",
            "username": "aa", # the min username length should be >= 3  
            "password": "anyvaildpassword" 
        }

    response = test_client.post("/api/v1/register", json=payload)
    assert response.status_code == 422

def test_register_username_too_long(test_client):
    payload = {
            "email": "test@test.com",
            "username": "a" * 21, # the max username length should be <= 20
            "password": "anyvaildpassword" 
        }

    response = test_client.post("/api/v1/register", json=payload)
    assert response.status_code == 422


def test_register_success(test_client):
    payload = {
        "email": "test@test.com",
        "username": "test_username",
        "password": "anyvalidpassword",
    }

    response = test_client.post("/api/v1/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "test_username"


def test_register_duplicate_email(test_client):
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }

    response1 = test_client.post("/api/v1/register", json=payload) # the first post to create a user 
    response2 = test_client.post("/api/v1/register", json=payload) # the second post will create a conflict of duplicate user 

    assert response1.status_code == 201
    assert response2.status_code == 409
