import pytest
import json
import asyncio
from datetime import datetime
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app
from app.config import settings
from app.database import Base, async_session_maker, engine_nullpool
from app.book.models import Book
from app.user.models import User


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine_nullpool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)
        
    user = open_mock_json('user')
    book = open_mock_json('book')

    for _ in user:
        _['created_at'] = datetime.strptime(_['created_at'], '%Y-%m-%d')

    for _ in book:
        _['date_pub'] = datetime.strptime(_['date_pub'], '%Y-%m-%d')

    async with async_session_maker() as session:        
        add_user = insert(User).values(user)
        add_book = insert(Book).values(book)

        await session.execute(add_user)
        await session.execute(add_book)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app),
                           base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authontificated_reader_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app),
                           base_url='http://test') as auth_reader_ac:
        await auth_reader_ac.post('/user/login', json={
            'email': 'random@example.com',
            'password': 'string'
        })

        assert auth_reader_ac.cookies['access_token'] 

        yield auth_reader_ac


@pytest.fixture(scope='session')
async def authontificated_admin_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app),
                           base_url='http://test') as auth_admin_ac:
        await auth_admin_ac.post('/user/login', json={
            'email': 'admin@example.com',
            'password': 'string'
        })

        assert auth_admin_ac.cookies['access_token'] 

        yield auth_admin_ac