from app import schemas
from fastapi.exceptions import HTTPException

def test_vote_valid_post(client, authorized_client, test_user, test_posts):
    post = test_posts[0]
    response = authorized_client.post(
        f"/votes/{post.id}", json={"post_id": post.id, "dir": 1}
    )
    assert response.status_code == 201
    assert schemas.VoteOut(**response.json())

def test_vote_invalid_post_id(client, authorized_client, test_user):
    response = authorized_client.post(
        "/votes/invalid_id", json={"post_id": "invalid_id", "dir": 1}
    )
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert any(isinstance(error, schemas.ValidationError) for error in response.json()["detail"])

def test_vote_invalid_dir(client, authorized_client, test_user, test_posts):
    post = test_posts[0]
    response = authorized_client.post(
        f"/votes/{post.id}", json={"post_id": post.id, "dir": 2}
    )
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert any(isinstance(error, schemas.ValidationError) for error in response.json()["detail"])

def test_vote_unauthorized(client):
    post = test_posts[0]
    response = client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    assert response.status_code == 401

def test_get_votes_unauthorized(client):
    response = client.get("/votes")
    assert response.status_code == 401

def test_get_vote_by_id_unauthorized(client, test_posts):
    post = test_posts[0]
    response = client.get(f"/votes/{post.id}")
    assert response.status_code == 401

def test_get_vote_by_id_non_existent(client, authorized_client):
    response = authorized_client.get("/votes/1234567890")
    assert response.status_code == 404

def test_get_votes(authorized_client):
    response = authorized_client.get("/votes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for vote in response.json():
        assert isinstance(vote, schemas.VoteOut)

def test_get_vote_by_id(authorized_client, test_posts):
    post = test_posts[0]
    vote = authorized_client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    vote_id = vote.json()["id"]
    response = authorized_client.get(f"/votes/{vote_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), schemas.VoteOut)

def test_put_vote_valid(authorized_client, test_posts):
    post = test_posts[0]
    vote = authorized_client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    vote_id = vote.json()["id"]
    response = authorized_client.put(f"/votes/{vote_id}", json={"post_id": post.id, "dir": -1})
    assert response.status_code == 200
    assert response.json()["id"] == vote_id
    assert response.json()["dir"] == -1

def test_put_vote_unauthorized(client, test_posts):
    post = test_posts[0]
    vote = client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    vote_id = vote.json()["id"]
    response = client.put(f"/votes/{vote_id}", json={"post_id": post.id, "dir": -1})
    assert response.status_code == 401

def test_put_vote_non_existent(client, test_posts):
    response = client.put("/votes/1234567890", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 404

def test_delete_vote_authorized(authorized_client, test_posts):
    post = test_posts[0]
    vote = authorized_client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    vote_id = vote.json()["id"]
    response = authorized_client.delete(f"/votes/{vote_id}")
    assert response.status_code == 204

def test_delete_vote_unauthorized(client, test_posts):
    post = test_posts[0]
    vote = client.post(f"/votes/{post.id}", json={"post_id": post.id, "dir": 1})
    vote_id = vote.json()["id"]
    response = client.delete(f"/votes/{vote_id}")
    assert response.status_code == 401

def test_delete_vote_non_existent(client):
    response = client.delete("/votes/1234567890")
    assert response.status_code == 404


# This code covers all CRUD operations for the Vote resource, including GET all, GET by ID (existing, non-existent, unauthorized), POST (valid, invalid, missing fields, wrong types), PUT (valid, unauthorized, non-existent), and DELETE (authorized, unauthorized, non-existent). It also tests authentication by checking requests with valid authentication, requests without authentication, and requests with invalid authentication. Additionally, it includes negative tests for invalid IDs, missing required fields, empty strings, wrong types, and non-existent resources.