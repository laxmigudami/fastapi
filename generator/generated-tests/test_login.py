from app import schemas
from fastapi.exceptions import HTTPException

def test_login_valid_credentials(authorized_client, test_user):
    response = authorized_client.post("/auth/login", data={"username": test_user.username, "password": test_user.password})
    assert response.status_code == 200
    assert schemas.Token(**response.json())

def test_login_invalid_credentials(authorized_client, test_user):
    response = authorized_client.post("/auth/login", data={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == HTTPException.unauthorized.status_code

def test_login_missing_credentials(authorized_client):
    response = authorized_client.post("/auth/login")
    assert response.status_code == HTTPException.unprocessable_entity.status_code
    assert response.json()["detail"][0]["loc"][0] == "login"

def test_create_user_valid(client, test_user):
    response = client.post("/users", json=test_user.dict())
    assert response.status_code == 201
    assert schemas.UserOut(**response.json())

def test_create_user_invalid(client):
    invalid_user = {
        "username": "",
        "email": "",
        "password": "",
    }
    response = client.post("/users", json=invalid_user)
    assert response.status_code == HTTPException.unprocessable_entity.status_code
    assert response.json()["detail"][0]["loc"][0] == "username"

def test_get_users_authorized(authorized_client):
    response = authorized_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for user in response.json():
        assert isinstance(user, dict)
        assert schemas.UserOut(**user)

def test_get_user_by_id_authorized(authorized_client, test_user):
    response = authorized_client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert schemas.UserOut(**response.json())

def test_get_user_by_id_non_existent(authorized_client):
    response = authorized_client.get("/users/-1")
    assert response.status_code == HTTPException.not_found.status_code

def test_get_user_by_id_unauthorized(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPException.unauthorized.status_code

def test_update_user_valid(authorized_client, test_user):
    updated_user = schemas.UserUpdate(username="updated_username", email="updated_email")
    response = authorized_client.put(f"/users/{test_user.id}", json=updated_user.dict())
    assert response.status_code == 200
    assert schemas.UserOut(**response.json())

def test_update_user_invalid(authorized_client, test_user):
    invalid_user = {
        "username": "",
        "email": "",
    }
    response = authorized_client.put(f"/users/{test_user.id}", json=invalid_user)
    assert response.status_code == HTTPException.unprocessable_entity.status_code
    assert response.json()["detail"][0]["loc"][0] == "username"

def test_update_user_unauthorized(client):
    response = client.put("/users/1")
    assert response.status_code == HTTPException.unauthorized.status_code

def test_delete_user_authorized(authorized_client, test_user):
    response = authorized_client.delete(f"/users/{test_user.id}")
    assert response.status_code == 204

def test_delete_user_unauthorized(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPException.unauthorized.status_code


# This code covers the login, create user, get users, get user by ID, update user, and delete user operations for the API. It uses the provided fixtures for the client, authorized_client, test_user, and token. The tests validate both the status code and response content based on the OpenAPI operation and the FastAPI schemas.