from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from app.config import settings
from app.user.router import router as router_user
from app.book.router import router as router_book
from app.author.router import router as router_author
from app.book_issuance.router import router as router_book_issuance


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(title='Support', lifespan=lifespan)


app.include_router(router_user)
app.include_router(router_book)
app.include_router(router_author)
app.include_router(router_book_issuance)


origins = [
    '*',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type',
                   'Set-Cookie',
                   'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Origin',
                   'Authorization'],
)