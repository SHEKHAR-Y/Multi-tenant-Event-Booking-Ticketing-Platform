import pytest
import uuid

from app.models.user import User

from app.repository.user import UserRepository

# two cases - 1. user exist 2. no user exist
def test_get_user_by_email_returns_user_when_exists(db_session):
    # create a user in db then try to fetch it by 
    test_user = User(
        email = "test@test.com",
        hashed_password = "any_valid_password",
        full_name = "test_name"
    )

    db_session.add(test_user)
    db_session.commit() # permanent the changes

    repo = UserRepository(db=db_session)
    result = repo.get_user_by_email(email="test@test.com")

    assert result.email == "test@test.com"

# user not exist 
def test_get_user_by_email_failure_none_when_user_does_not_exists(db_session):
    repo = UserRepository(db=db_session)
    result = repo.get_user_by_email(email="test@test.com")

    assert result == None

# test get user by id same 2 cases as above - 1. user exist 2. no user exist
def test_get_user_by_id_returns_user_when_exists(db_session):
    # create a user in db then try to fetch it by 
    test_user = User(
        email = "test@test.com",
        hashed_password = "any_valid_password",
        full_name = "test_name"
    )

    db_session.add(test_user)
    db_session.commit() # permanent the changes
    db_session.refresh(test_user)

    repo = UserRepository(db=db_session)
    result = repo.get_user_by_id(id=test_user.id)

    assert result.email == "test@test.com"
    assert result.full_name == "test_name"
    assert result.id == test_user.id
    assert result.hashed_password == test_user.hashed_password

def test_get_user_by_id_returns_none_when_user_does_not_exists(db_session):
    test_id = uuid.uuid4()
    repo = UserRepository(db=db_session)
    result = repo.get_user_by_id(id=test_id)

    assert result == None
    # changes done only for docker 
    print("a")
# test create user
def test_create_user_returns_user_when_success(db_session):
    test_user = User(
        email = "test@test.com",
        hashed_password = "any_valid_password",
        full_name = "test_name"
    )

    userrepo = UserRepository(db=db_session)
    result = userrepo.create_user(test_user)

    assert result.email == test_user.email
    assert result.full_name == test_user.full_name

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...

# def test_create_refresh_token_return_refresh_token_when_success(db_session):
#     ...
