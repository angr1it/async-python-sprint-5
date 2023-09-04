import json

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_file_upload(client: AsyncClient):

    test_file = open("tests/data/test.json", "rb")
    response = await client.post(
        url=app.url_path_for('upload_file'),
        files={'file': test_file},
    )

    data = json.loads(response.content)
    assert response.status_code == 200
    assert data['name'] == 'test.json'
    assert data['path'] == 'test.json'

    test_file = open("tests/data/test2.json", "rb")
    response = await client.post(
        url=app.url_path_for('upload_file'),
        params={'directory_path': '/home'},
        files={'file': test_file},
    )

    data = json.loads(response.content)
    assert response.status_code == 200
    assert data['name'] == 'test2.json'
    assert data['path'] == '/home/test2.json'


@pytest.mark.anyio
async def test_show_files(client: AsyncClient):
    await client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=writer@test.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response = await client.get(
        url=app.url_path_for('show_files'),
        params={'limit': '1'},
    )

    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['path'] == 'test.json'

    response = await client.get(
        url=app.url_path_for('show_files'),
        params={'limit': 1, 'offset': 1},
    )

    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 1
    assert data[0]['path'] == '/home/test2.json'

    await client.post(
        url=app.url_path_for('auth:jwt.logout'),
    )

    response = await client.get(
        url=app.url_path_for('show_files'),
    )

    assert response.status_code == 401
    data = json.loads(response.content)
    assert data['detail'] == 'Unauthorized'


@pytest.mark.anyio
async def test_download(client: AsyncClient):
    await client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=user@example.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    response = await client.get(
        url=app.url_path_for('download_file'),
        params={'file_path': 'test.json'}
    )

    assert response.status_code == 200
    assert response.content == b'{\n    "data": "secret"\n}'
