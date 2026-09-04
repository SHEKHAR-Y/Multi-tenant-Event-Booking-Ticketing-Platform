import pytest 

def test_login_success(test_client):
    # create a user for testing
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    
    response1 = test_client.post("/api/v1/register", json=payload)
    assert response1.status_code == 201
    data = response1.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "test_username"


    response2 = test_client.post(
        "/api/v1/login",
          data={
                "username": "test@test.com", 
                "password": "anyvalidpassword"
            }
        )
    assert response2.status_code == 200

def test_login_failure_invalid_email(test_client):
    """
    for the wrong email format or the email not registered it will give same error to not explitly
    state the issue to avoid exploitation of any gap
    """
    response = test_client.post(
        "/api/v1/login", 
        data={
            "username": "test.com", 
            "password": "anyvalidpassword"
            },
        )
    assert response.status_code == 404


def test_login_failure_incorrect_password(test_client):
    # create a user for testing
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    
    response1 = test_client.post("/api/v1/register", json=payload)
    assert response1.status_code == 201
    data = response1.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "test_username"

    response2 = test_client.post(
        "/api/v1/login", 
        data={
            "username": "test@test.com",
            "password": "wrongpassword",
            }
        )

    assert response2.status_code == 401