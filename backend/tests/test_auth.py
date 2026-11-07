from tests.conftest import get_auth_header


def test_user_registration(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "anita.weaver@shg.org",
        "password": "Password123!",
        "full_name": "Anita Weaver",
        "role": "SHG_MEMBER",
        "phone": "+919988776655"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["success"] is True
    assert data["data"]["email"] == "anita.weaver@shg.org"
    assert data["data"]["role"] == "SHG_MEMBER"


def test_user_login(client, leader_user):
    res = client.post("/api/v1/auth/login", data={
        "username": leader_user.email,
        "password": "password123"
    })
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["user"]["role"] == "SHG_LEADER"


def test_unauthorized_access(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401


def test_me_endpoint_with_auth(client, leader_user):
    headers = get_auth_header(leader_user)
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["email"] == leader_user.email
