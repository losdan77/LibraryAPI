import pytest
from httpx import AsyncClient


async def test_add_book_issuance(authontificated_reader_ac: AsyncClient):
    response = await authontificated_reader_ac.post('/book_issuance/add_book_issuance', json={
        "id_book": 1,
        "return_date": "2030-01-22"
    })    

    assert response.status_code == 200


async def test_get_my_book(authontificated_reader_ac: AsyncClient):
    reponse = await authontificated_reader_ac.get('/book_issuance/get_my_book')

    assert len(reponse.json()) == 1


async def test_return_book(authontificated_reader_ac: AsyncClient):
    response = await authontificated_reader_ac.post('/book_issuance/return_book', params={
        "id_book": 1
    })    

    assert response.status_code == 200


@pytest.mark.parametrize('id_book,return_date,status_code', [
    (1, '2030-01-22', 200),
    (1, '2030-01-22', 200),
    (1, '2030-01-22', 404),
])
async def test_error_add_book_issuance(id_book, return_date, status_code, authontificated_reader_ac: AsyncClient):
    response = await authontificated_reader_ac.post('/book_issuance/add_book_issuance', json={
        "id_book": id_book,
        "return_date": return_date
    })    

    assert response.status_code == status_code


