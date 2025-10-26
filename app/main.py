from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis

from app.routes import auth_routes, customer_routes, loanoffer_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    yield
    redis_client.close()

app = FastAPI(title="Bees & Bears Backend")

app.include_router(auth_routes.router)
app.include_router(customer_routes.router)
app.include_router(loanoffer_routes.router)
