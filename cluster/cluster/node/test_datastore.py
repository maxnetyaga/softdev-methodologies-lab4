import random
import pytest
import humanfriendly
from .datastore import Datastore


@pytest.fixture
def ds():
    return Datastore()


# ---------- String Tests ----------


def test_str_set_get(ds):
    assert ds.strset('key', 'value') is True
    assert ds.strget('key') == 'value'
    assert ds.strget('nonexistent') is None


def test_str_overwrite(ds):
    ds.strset('k', '1')
    ds.strset('k', '2')
    assert ds.strget('k') == '2'


# ---------- List Tests ----------


def test_lpush_rpush_lrange(ds):
    assert ds.lpush('list', 'a', '') == 2
    assert ds.rpush('list', 'c') == 3
    assert ds.lrange('list', 0, -1) == ['', 'a', 'c']
    assert ds.lrange('list', 1, 1) == ['a']
    assert ds.lrange('list', 10, 20) == []


def test_lpush_create_new(ds):
    ds.lpush('newlist', 'x')
    assert ds.lrange('newlist', 0, -1) == ['x']


# ---------- Set Tests ----------


def test_sadd_smembers(ds):
    assert ds.sadd('set', 'a', '') == 2
    assert ds.sadd('set', '', 'c') == 1
    members = ds.smembers('set')
    assert members == {'a', '', 'c'}


def test_smembers_empty(ds):
    assert ds.smembers('empty') == set()


# ---------- Hash Tests ----------


def test_hset_hget(ds):
    assert ds.hset('hash', 'f1', 'v1') == 1
    assert ds.hset('hash', 'f1', 'v2') == 0
    assert ds.hget('hash', 'f1') == 'v2'
    assert ds.hget('hash', 'f2') is None


def test_hgetall(ds):
    ds.hset('h', 'k1', 'v1')
    ds.hset('h', 'k2', 'v2')
    assert ds.hgetall('h') == {'k1': 'v1', 'k2': 'v2'}


# ---------- Sorted Set Tests ----------


def test_zadd_zrange(ds):
    mapping = {'a': 1.0, '': 0.5}
    assert ds.zadd('zset', mapping) == 2
    assert ds.zadd('zset', {'a': 2.0}) == 0
    assert ds.zrange('zset', 0, -1) == ['', 'a']


def test_zrange_with_score(ds):
    ds.zadd('z', {'x': 1.5, 'y': 0.1})
    assert ds.zrange('z', 0, -1, withscores=True) == [('y', 0.1), ('x', 1.5)]


# ---------- Delete ----------


def test_delete_existing():
    ds = Datastore()

    ds.strset('dkey', 'dval')
    assert ds.delete('dkey') == 1
    assert ds.size == 0
    assert ds.strget('dkey') is None


def test_delete_nonexistent(ds):
    assert ds.delete('missing') == 0


# ---------- Complex test ----------


def gen_str(size: int) -> str:
    return 'a' * size


@pytest.mark.long
def test_memory_budget_():
    ds = Datastore()

    target_bytes = humanfriendly.parse_size('1G')
    sharding = 0.005
    shard_size = int(target_bytes * sharding)

    keys = []
    i = 0

    # ADD
    while ds.size < target_bytes:
        key = f'k{i}'
        typ = random.randint(0, 4)

        if typ == 0:
            val = gen_str(shard_size)
            ds.strset(key, val)
        elif typ == 1:
            ds.lpush(key, gen_str(shard_size // 2), gen_str(shard_size // 2))
        elif typ == 2:
            ds.sadd(key, gen_str(shard_size // 2), gen_str(shard_size // 2))
        elif typ == 3:
            ds.hset(key, 'field', gen_str(shard_size))
        elif typ == 4:
            ds.zadd(key, {gen_str(shard_size): float(i)})

        keys.append(key)
        i += 1

    print(
        f'Created {len(keys)} keys consuming {humanfriendly.format_size(ds.size)}'
    )

    # REPLACE
    for i, key in enumerate(keys):
        typ = random.randint(0, 4)
        if typ == 0:
            ds.strset(key, f'replaced_{i}')
        elif typ == 1:
            ds.rpush(key, f'tail_{i}')
        elif typ == 2:
            ds.sadd(key, f'new_{i}')
        elif typ == 3:
            ds.hset(key, 'field', f'replaced_{i}')
        elif typ == 4:
            ds.zadd(key, {f'newm{i}': float(i + 0.5)})

    # DELETE
    deleted = sum(ds.delete(k) for k in keys)
    assert deleted == len(keys)
    assert ds.size == 0
