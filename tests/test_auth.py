import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_register(client: AsyncClient):
    response = await client.post(
        url=app.url_path_for('register:register'),
        json={
            "username": "user",
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 201


@pytest.mark.anyio
async def test_login(client: AsyncClient):
    response = await client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=user@example.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 204
