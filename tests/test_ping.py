import json

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_ping_anonymus(client: AsyncClient):
    response = await client.get(
        url=app.url_path_for('get_ping'),
    )

    data = json.loads(response.content)
    assert data["status"] == "OK"
    assert not data["data"]["services"]["db"] is None
    assert not data["data"]["services"]["redis"] is FileNotFoundError


@pytest.mark.anyio
async def test_ping_logged(client: AsyncClient):
    response = await client.post(
        url=app.url_path_for('register:register'),
        json={
            "username": "ping",
            "email": "ping@test.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 201

    response = await client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=ping@test.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 204
    login_cookie = response.cookies

    response = await client.get(
        url=app.url_path_for('get_ping'),
        cookies=login_cookie
    )

    data = json.loads(response.content)
    assert data["data"]["user"] == "ping@test.com"

    response = await client.post(
        url=app.url_path_for('auth:jwt.logout'),
        cookies=login_cookie
    )

    assert response.status_code == 204
