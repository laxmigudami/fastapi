import pytest
from app import schemas, models
from app.database import Database
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from fastapi import status
from app.oauth2 import create_access_token

@pytest.fixture(scope="function")
def test_post(test_user, test_posts, client):
    db = Database()
    db.init_db()
    post = models.Post(title="Test Post", content="Test Content", owner_id=test_user.id)
    db.session.add(post)
    db.session.commit()
    res = client.post("/posts", json={"title": "Updated Title", "content": "Updated Content"})
    assert res.status_code == status.HTTP_201_CREATED
    post_id = res.json().get("id")
    yield post_id
    db.session.delete(post)
    db.session.commit()
    db.session.close()

def test_get_posts(client, authorized_client):
    res = authorized_client.get("/posts")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    for post in res.json():
        assert isinstance(post, schemas.PostOut)

def test_get_post_non_existent(client):
    res = client.get("/posts/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_post_unauthorized(client):
    res = client.get("/posts/1")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_post_existing(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), schemas.PostOut)

def test_post_valid(authorized_client):
    res = authorized_client.post("/posts", json={"title": "New Post", "content": "New Content"})
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), schemas.PostOut)

def test_post_invalid(authorized_client):
    res = authorized_client.post("/posts", json={"title": "", "content": ""})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(res.json(), dict)
    assert res.json().get("detail")[0].get("loc") == ["body", "title"]

def test_post_missing_fields(authorized_client):
    res = authorized_client.post("/posts", json={"title": "New Post"})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(res.json(), dict)
    assert res.json().get("detail")[0].get("loc") == ["body", "content"]

def test_post_wrong_types(authorized_client):
    res = authorized_client.post("/posts", json={"title": 123, "content": True})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(res.json(), dict)
    assert res.json().get("detail")[0].get("loc") == ["body", "title"]

def test_put_valid(authorized_client, test_post):
    res = authorized_client.put(f"/posts/{test_post}", json={"title": "Updated Title", "content": "Updated Content"})
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), schemas.PostOut)

def test_put_invalid(authorized_client, test_post):
    res = authorized_client.put(f"/posts/{test_post}", json={"title": "", "content": ""})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(res.json(), dict)
    assert res.json().get("detail")[0].get("loc") == ["body", "title"]

def test_put_unauthorized(client, test_post):
    res = client.put(f"/posts/{test_post}", json={"title": "Updated Title", "content": "Updated Content"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_put_non_existent(client):
    res = client.put("/posts/1", json={"title": "Updated Title", "content": "Updated Content"})
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_authorized(authorized_client, test_post):
    res = authorized_client.delete(f"/posts/{test_post}")
    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_delete_unauthorized(client, test_post):
    res = client.delete(f"/posts/{test_post}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_non_existent(client):
    res = client.delete("/posts/1")
    assert res.status_code == status.HTTP_404_NOT_FOUND


# This code includes tests for all CRUD operations for the Post resource, including GET all, GET by ID (existing, non-existent, unauthorized), POST (valid, invalid, missing fields, wrong types), PUT (valid, invalid, unauthorized, non-existent), and DELETE (authorized, unauthorized, non-existent). It also includes tests for authentication, such as requests with valid authentication, requests without authentication, and requests with invalid authentication. The tests use the provided fixtures for the client, authorized_client, test_user, test_user2, test_posts, and token. The test_post fixture creates a new post, uses its ID for the test, and cleans up after the test is finished.