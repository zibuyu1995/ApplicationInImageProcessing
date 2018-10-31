# coding: utf-8

from aioredis import create_redis

from config.config import redis_address


async def connect_redis():
    redis_store = await create_redis(redis_address)
    return redis_store
