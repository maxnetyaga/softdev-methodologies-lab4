from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .manager import Manager, Node, NodeSettings


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ds
    ds = Manager()
    node = Node(NodeSettings(address='0.0.0.0', port=9063, role='shard'))
    ds.add_node(node)
    app.state
    yield


app = FastAPI(lifespan=lifespan)


# ------------------ STRING ------------------ #
class StringSetRequest(BaseModel):
    key: str
    value: str


class StringGetRequest(BaseModel):
    key: str


@app.post('/strset/')
async def set_string(data: StringSetRequest) -> bool:
    return await ds.strset(data.key, data.value)


@app.post('/strget/')
async def get_string(data: StringGetRequest) -> str:
    val = await ds.strget(data.key)
    return val


# ------------------ LIST ------------------ #
class ListPushRequest(BaseModel):
    key: str
    values: list[str]


@app.post('/list/rpush/')
async def rpush_list(data: ListPushRequest):
    await ds.rpush(data.key, *data.values)
    return {
        'status': 'ok',
        'method': 'RPUSH',
        'key': data.key,
        'values': data.values,
    }


@app.post('/list/lpush/')
async def lpush_list(data: ListPushRequest):
    await ds.lpush(data.key, *data.values)
    return {
        'status': 'ok',
        'method': 'LPUSH',
        'key': data.key,
        'values': data.values,
    }


@app.get('/list/')
async def get_list(key: str, start: int = 0, end: int = -1):
    items = await ds.lrange(key, start, end)
    return {'key': key, 'range': [start, end], 'values': items}


# ------------------ SET ------------------ #
class SetRequest(BaseModel):
    key: str
    members: list[str]


@app.post('/set/')
async def add_set(data: SetRequest):
    await ds.sadd(data.key, *data.members)
    return {'status': 'ok'}


@app.get('/set/')
async def get_set(key: str):
    return {'key': key, 'members': list(await ds.smembers(key))}


# ------------------ HASH ------------------ #
class HashRequest(BaseModel):
    key: str
    fields: dict[str, str]


@app.post('/hash/')
async def set_hash(data: HashRequest):
    await ds.hset(data.key, mapping=data.fields)
    return {'status': 'ok'}


@app.get('/hash/')
async def get_hash(key: str, field: str | None = None):
    if field:
        val = await ds.hget(key, field)
        if val is None:
            raise HTTPException(status_code=404, detail='Field not found')
        return {'field': field, 'value': val}
    return await ds.hgetall(key)


# ------------------ SORTED SET ------------------ #
class ZSetRequest(BaseModel):
    key: str
    members: dict[str, float]


@app.post('/zset/')
async def add_zset(data: ZSetRequest):
    await ds.zadd(data.key, data.members)
    return {'status': 'ok'}


@app.get('/zset/')
async def get_zset(
    key: str, start: int = 0, end: int = -1, withscores: bool = True
):
    items = await ds.zrange(key, start, end, withscores=withscores)
    if withscores:
        return [{'member': m, 'score': s} for m, s in items]
    else:
        return {'members': items}
