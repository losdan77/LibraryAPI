from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    response = await ac.post('/user/registr', json={
        "email": "test@example.com",
        "password": "string",
        "password_verify": "string",
        "name": "string",
        "role": "reader"
    })    

    assert response.status_code == 200


async def test_login_user(ac: AsyncClient):
    response = await ac.post('/user/login', json={
        "email": "test@example.com",
        "password": "string"
    })    

    assert response.status_code == 200


async def test_error_reader_get_all_users(authontificated_reader_ac: AsyncClient):
    response = await authontificated_reader_ac.get('/user/get_all_users')    

    assert response.status_code == 403


async def test_admin_get_all_users(authontificated_admin_ac: AsyncClient):
    response = await authontificated_admin_ac.get('/user/get_all_users')    

    assert response.status_code == 200