import pytest


@pytest.fixture()
def user(client):
    res = client.post("/users/register", json={
        "username": "calcuser",
        "email": "calcuser@example.com",
        "first_name": "Calc",
        "last_name": "User",
        "password": "calcpass123"
    })
    return res.json()


def test_add(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "add", "inputs": {"a": 10, "b": 5}
    })
    assert res.status_code == 201
    assert res.json()["result"] == 15.0


def test_subtract(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "subtract", "inputs": {"a": 20, "b": 8}
    })
    assert res.status_code == 201
    assert res.json()["result"] == 12.0


def test_multiply(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "multiply", "inputs": {"a": 4, "b": 7}
    })
    assert res.status_code == 201
    assert res.json()["result"] == 28.0


def test_divide(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "divide", "inputs": {"a": 20, "b": 4}
    })
    assert res.status_code == 201
    assert res.json()["result"] == 5.0


def test_divide_by_zero(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "divide", "inputs": {"a": 10, "b": 0}
    })
    assert res.status_code == 400
    assert "divide by zero" in res.json()["detail"].lower()


def test_invalid_operation(client, user):
    res = client.post("/calculations/", json={
        "user_id": user["id"], "type": "modulo", "inputs": {"a": 10, "b": 3}
    })
    assert res.status_code == 400


def test_user_not_found(client):
    res = client.post("/calculations/", json={
        "user_id": 99999, "type": "add", "inputs": {"a": 1, "b": 2}
    })
    assert res.status_code == 404


def test_browse(client, user):
    client.post("/calculations/", json={
        "user_id": user["id"], "type": "add", "inputs": {"a": 1, "b": 1}
    })
    res = client.get("/calculations/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1


def test_read(client, user):
    create = client.post("/calculations/", json={
        "user_id": user["id"], "type": "add", "inputs": {"a": 3, "b": 3}
    })
    calc_id = create.json()["id"]
    res = client.get(f"/calculations/{calc_id}")
    assert res.status_code == 200
    assert res.json()["id"] == calc_id


def test_read_not_found(client):
    res = client.get("/calculations/99999")
    assert res.status_code == 404


def test_edit(client, user):
    create = client.post("/calculations/", json={
        "user_id": user["id"], "type": "add", "inputs": {"a": 5, "b": 5}
    })
    calc_id = create.json()["id"]
    res = client.put(f"/calculations/{calc_id}", json={
        "type": "multiply", "inputs": {"a": 3, "b": 4}
    })
    assert res.status_code == 200
    assert res.json()["result"] == 12.0


def test_delete(client, user):
    create = client.post("/calculations/", json={
        "user_id": user["id"], "type": "add", "inputs": {"a": 2, "b": 2}
    })
    calc_id = create.json()["id"]
    res = client.delete(f"/calculations/{calc_id}")
    assert res.status_code == 204
    res2 = client.get(f"/calculations/{calc_id}")
    assert res2.status_code == 404
