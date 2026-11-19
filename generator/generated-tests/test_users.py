from app import schemas, models
from fastapi.exceptions import HTTPException

def test_create_user_valid(client, test_user, token):
    res = client.post("/users", json={"email": test_user.email, "password": test_user.hashed_password})
    assert res.status_code == 201
    assert schemas.UserOut(**res.json())

def test_create_user_invalid_email(client, token):
    res = client.post("/users", json={"email": "invalid_email", "password": test_user.hashed_password})
    assert res.status_code == 422
    assert res.json() == {"detail": [{"loc": ["email"], "msg": "Email must be a valid email address"}]}}

def test_create_user_invalid_password(client, token):
    res = client.post("/users", json={"email": test_user.email, "password": "short_password"})
    assert res.status_code == 422
    assert res.json() == {"detail": [{"loc": ["password"], "msg": "Password must be at least 8 characters"}]}}

def test_login_valid(client, test_user, token):
    res = client.post("/login", json={"email": test_user.email, "password": test_user.password})
    assert res.status_code == 200
    assert res.json()["access_token"] == token
    assert schemas.Token(**res.json()["token_data"])

def test_login_invalid_email(client):
    res = client.post("/login", json={"email": "invalid_email", "password": test_user.password})
    assert res.status_code == 401

def test_login_invalid_password(client):
    res = client.post("/login", json={"email": test_user.email, "password": "wrong_password"})
    assert res.status_code == 401

def test_get_all_users_authorized(authorized_client):
    res = authorized_client.get("/users")
    assert res.status_code == 200
    for user in res.json():
        assert schemas.UserOut(**user)

def test_get_user_by_id_existing(authorized_client, test_user):
    res = authorized_client.get(f"/users/{test_user.id}")
    assert res.status_code == 200
    assert schemas.UserOut(**res.json())

def test_get_user_by_id_non_existent(authorized_client):
    res = authorized_client.get("/users/0")
    assert res.status_code == 404

def test_get_user_by_id_unauthorized(client):
    res = client.get(f"/users/{test_user.id}")
    assert res.status_code == 401

def test_post_user_valid(client, token):
    res = client.post("/users", json={"email": "new_user@example.com", "password": "new_password"})
    assert res.status_code == 201
    assert schemas.UserOut(**res.json())

def test_post_user_invalid_email(client, token):
    res = client.post("/users", json={"email": "invalid_email", "password": "new_password"})
    assert res.status_code == 422
    assert res.json() == {"detail": [{"loc": ["email"], "msg": "Email must be a valid email address"}]}}

def test_post_user_invalid_password(client, token):
    res = client.post("/users", json={"email": "new_user@example.com", "password": "short_password"})
    assert res.status_code == 422
    assert res.json() == {"detail": [{"loc": ["password"], "msg": "Password must be at least 8 characters"}]}}

def test_put_user_valid(authorized_client, test_user):
    new_email = "updated_user@example.com"
    res = authorized_client.put(f"/users/{test_user.id}", json={"email": new_email})
    assert res.status_code == 200
    assert res.json()["email"] == new_email

def test_put_user_invalid_email(authorized_client, test_user):
    new_email = "invalid_email"
    res = authorized_client.put(f"/users/{test_user.id}", json={"email": new_email})
    assert res.status_code == 422
    assert res.json() == {"detail": [{"loc": ["email"], "msg": "Email must be a valid email address"}]}}

def test_put_user_unauthorized(client):
    new_email = "updated_user@example.com"
    res = client.put(f"/users/{test_user.id}", json={"email": new_email})
    assert res.status_code == 401

def test_delete_user_authorized(authorized_client, test_user):
    res = authorized_client.delete(f"/users/{test_user.id}")
    assert res.status_code == 204

def test_delete_user_unauthorized(client):
    res = client.delete(f"/users/{test_user.id}")
    assert res.status_code == 401


# This code covers all the requirements mentioned in your question, including creating, logging in, and testing CRUD operations for the User resource. Make sure to adjust the imports and fixture names according to your project structure and naming conventions.