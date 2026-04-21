def test_register_success(client):
    res = client.post("/users/register", json={
        "username": "ketan",
        "email": "ketan@example.com",
        "first_name": "Ketan",
        "last_name": "Verma",
        "password": "securepass123"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "ketan"
    assert data["email"] == "ketan@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    payload = {
        "username": "dupuser",
        "email": "dup1@example.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "pass123"
    }
    client.post("/users/register", json=payload)
    payload["email"] = "dup2@example.com"
    res = client.post("/users/register", json=payload)
    assert res.status_code == 400
    assert "Username already exists" in res.json()["detail"]


def test_register_duplicate_email(client):
    payload = {
        "username": "user1",
        "email": "shared@example.com",
        "first_name": "A",
        "last_name": "B",
        "password": "pass123"
    }
    client.post("/users/register", json=payload)
    payload["username"] = "user2"
    res = client.post("/users/register", json=payload)
    assert res.status_code == 400
    assert "Email already exists" in res.json()["detail"]


def test_register_invalid_email(client):
    res = client.post("/users/register", json={
        "username": "bademail",
        "email": "not-an-email",
        "first_name": "Bad",
        "last_name": "Email",
        "password": "pass123"
    })
    assert res.status_code == 422


def test_login_success(client):
    client.post("/users/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "first_name": "Login",
        "last_name": "User",
        "password": "mypassword"
    })
    res = client.post("/users/login", json={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert res.status_code == 200
    assert res.json()["message"] == "Login successful"
    assert res.json()["username"] == "loginuser"


def test_login_wrong_password(client):
    client.post("/users/register", json={
        "username": "wrongpass",
        "email": "wp@example.com",
        "first_name": "Wrong",
        "last_name": "Pass",
        "password": "correctpass"
    })
    res = client.post("/users/login", json={
        "username": "wrongpass",
        "password": "badpass"
    })
    assert res.status_code == 401


def test_login_nonexistent_user(client):
    res = client.post("/users/login", json={
        "username": "ghost",
        "password": "doesntmatter"
    })
    assert res.status_code == 401
