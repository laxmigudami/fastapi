from app import schemas
from fastapi.exceptions import HTTPException

def test_root_get_all(client):
    response = client.get("/")
    assert response.status_code == 200
    assert schemas.RootOut(**response.json())

def test_root_get_id_existing(client, test_posts):
    post = test_posts
    response = client.get(f"/{post.id}")
    assert response.status_code == 200
    assert schemas.PostOut(**response.json())

def test_root_get_id_non_existent(client):
    response = client.get("/123")
    assert response.status_code == HTTPException.unauthorized.status_code

def test_root_get_id_unauthorized(client):
    response = authorized_client.get("/123")
    assert response.status_code == HTTPException.unauthorized.status_code

def test_root_post_valid(authorized_client, test_user):
    data = schemas.PostCreate(title="Test Title", content="Test Content")
    response = authorized_client.post("/", json=data.dict())
    assert response.status_code == 201
    assert schemas.PostOut(**response.json())

def test_root_post_invalid(authorized_client):
    data = {
        "title": "Test Title",
        "content": 123,
    }
    response = authorized_client.post("/", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_root_post_missing_fields(authorized_client):
    data = {
        "title": "Test Title",
    }
    response = authorized_client.post("/", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_root_post_wrong_types(authorized_client):
    data = {
        "title": 123,
        "content": "Test Content",
    }
    response = authorized_client.post("/", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_root_put_valid(authorized_client, test_posts):
    post = test_posts
    data = schemas.PostUpdate(title="Updated Title", content="Updated Content")
    response = authorized_client.put(f"/{post.id}", json=data.dict())
    assert response.status_code == 200
    assert schemas.PostOut(**response.json())

def test_root_put_invalid(authorized_client, test_posts):
    post = test_posts
    data = {
        "title": "Updated Title",
        "content": 123,
    }
    response = authorized_client.put(f"/{post.id}", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_root_put_unauthorized(authorized_client):
    response = unauthorized_client.put("/1", json={})
    assert response.status_code == HTTPException.unauthorized.status_code

def test_root_put_non_existent(unauthorized_client):
    response = unauthorized_client.put("/123", json={})
    assert response.status_code == HTTPException.not_found.status_code

def test_root_delete_authorized(authorized_client, test_posts):
    post = test_posts
    response = authorized_client.delete(f"/{post.id}")
    assert response.status_code == 204

def test_root_delete_unauthorized(unauthorized_client):
    response = unauthorized_client.delete("/1")
    assert response.status_code == HTTPException.unauthorized.status_code

def test_root_delete_non_existent(unauthorized_client):
    response = unauthorized_client.delete("/123")
    assert response.status_code == HTTPException.not_found.status_code

def test_login_valid(client):
    data = {
        "username": "test_user",
        "password": "test_password",
    }
    response = client.post("/login", json=data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token_verification(token)

def test_login_invalid_username(client):
    data = {
        "username": "invalid_user",
        "password": "test_password",
    }
    response = client.post("/login", json=data)
    assert response.status_code == HTTPException.unauthorized.status_code

def test_login_invalid_password(client):
    data = {
        "username": "test_user",
        "password": "invalid_password",
    }
    response = client.post("/login", json=data)
    assert response.status_code == HTTPException.unauthorized.status_code

def test_create_user_valid(authorized_client):
    data = {
        "username": "test_user2",
        "email": "test_user2@example.com",
        "password": "test_password",
    }
    response = authorized_client.post("/users", json=data)
    assert response.status_code == 201
    assert schemas.UserOut(**response.json())

def test_create_user_invalid_username(authorized_client):
    data = {
        "username": "123",
        "email": "test_user2@example.com",
        "password": "test_password",
    }
    response = authorized_client.post("/users", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_create_user_invalid_email(authorized_client):
    data = {
        "username": "test_user2",
        "email": "test_user2",
        "password": "test_password",
    }
    response = authorized_client.post("/users", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code

def test_create_user_invalid_password(authorized_client):
    data = {
        "username": "test_user2",
        "email": "test_user2@example.com",
        "password": 123,
    }
    response = authorized_client.post("/users", json=data)
    assert response.status_code == HTTPException.unprocessable_entity.status_code


# This code includes tests for the root resource, covering GET all, GET by ID (existing, non-existent, unauthorized), POST (valid, invalid, missing fields, wrong types), PUT (valid, invalid, unauthorized, non-existent), and DELETE (authorized, unauthorized, non-existent). It also includes tests for login and creating a user. The `token_verification` function is assumed to be defined elsewhere to validate JWT tokens using the secret key and algorithm from app/config.py.