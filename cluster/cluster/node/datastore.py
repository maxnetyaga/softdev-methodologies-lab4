from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, overload
from .doubly_linked_list import DoublyLinkedList
import humanfriendly
import gc
from pympler import asizeof


@dataclass
class StoreItem:
    item: Any
    size: int


class Store:
    def __init__(self, max_size: int | None = None) -> None:
        self._max_size = max_size
        self._store: dict[str, StoreItem] = {}
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def __len__(self):
        return len(self._store)

    def __contains__(self, name: str) -> bool:
        return name in self._store

    def __getitem__(self, name: str) -> Any:
        return self._store[name].item

    def get(self, name: str, default: Any = None) -> Any:
        if name not in self._store:
            return default
        return self._store[name].item

    def __delitem__(self, name: str):
        self._size -= self._store[name].size
        del self._store[name]
        gc.collect()

    def pop(self, name, default=None) -> Any:
        if name not in self:
            return default

        value = self[name]
        self.__delitem__(name)
        return value

    def __setitem__(self, name: str, value: Any) -> Any:
        if name in self._store:
            self.__delitem__(name)

        val_size = asizeof.asizeof(value)
        store_size = self._size + val_size
        if self._max_size and store_size >= self._max_size:
            raise Exception()

        self._size = store_size
        self._store[name] = StoreItem(item=value, size=val_size)


class Datastore:
    def __init__(self, max_size: int = humanfriendly.parse_size('1G')) -> None:
        self._store: Store = Store(max_size=None)

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    @property
    def size(self) -> int:
        return self._store.size

    # String #

    def strset(self, key: str, value: str) -> bool:
        self._store[key] = value
        return True

    def strget(self, key: str) -> str | None:
        value = self._store.get(key)
        return value if isinstance(value, str) else None

    # List #

    def lpush(self, key: str, *values: str) -> int:
        if key not in self._store or not isinstance(
            self._store[key], DoublyLinkedList
        ):
            self._store[key] = DoublyLinkedList()
        return self._store[key].lpush(*values)

    def rpush(self, key: str, *values: str) -> int:
        if key not in self._store or not isinstance(
            self._store[key], DoublyLinkedList
        ):
            self._store[key] = DoublyLinkedList()
        return self._store[key].rpush(*values)

    def lrange(self, key: str, start: int, end: int) -> list[str]:
        if key not in self._store or not isinstance(
            self._store[key], DoublyLinkedList
        ):
            return []
        return self._store[key].lrange(start, end)

    # Set #

    def sadd(self, key: str, *members: str) -> int:
        if key not in self._store or not isinstance(self._store[key], set):
            self._store[key] = set()

        before = len(self._store[key])

        self._store[key].update(members)
        self._store[key] = self._store[key]

        return len(self._store[key]) - before

    def smembers(self, key: str) -> set[str]:
        return (
            self._store.get(key, set())
            if isinstance(self._store.get(key), set)
            else set()
        )

    # Hash #

    @overload
    def hset(
        self, key: str, field: str, value: str, *, mapping: None = ...
    ) -> int: ...

    @overload
    def hset(
        self,
        key: str,
        field: None = ...,
        value: None = ...,
        *,
        mapping: dict[str, str],
    ) -> int: ...

    def hset(
        self,
        key: str,
        field: str | None = None,
        value: str | None = None,
        *,
        mapping: dict[str, str] | None = None,
    ) -> int:
        if mapping is not None:
            if field is not None or value is not None:
                raise TypeError(
                    'Specify either field+value or mapping, not both'
                )
            if key not in self._store or not isinstance(self._store[key], dict):
                self._store[key] = {}
            new_fields = 0
            for f, v in mapping.items():
                if f not in self._store[key]:
                    new_fields += 1
                self._store[key][f] = v
            return new_fields
        elif field is not None and value is not None:
            if key not in self._store or not isinstance(self._store[key], dict):
                self._store[key] = {}
            is_new = field not in self._store[key]
            self._store[key][field] = value

            self._store[key] = self._store[key]
            return int(is_new)
        else:
            raise TypeError('You must specify either field+value or mapping')

    def hget(self, key: str, field: str) -> str | None:
        return (
            self._store.get(key, {}).get(field)
            if isinstance(self._store.get(key), dict)
            else None
        )

    def hgetall(self, key: str) -> dict[str, str]:
        return (
            self._store.get(key, {})
            if isinstance(self._store.get(key), dict)
            else {}
        )

    # Sorted set #

    def zadd(self, key: str, mapping: dict[str, float]) -> int:
        if key not in self._store or not isinstance(self._store[key], dict):
            self._store[key] = {}
        added = 0
        for member, score in mapping.items():
            if member not in self._store[key]:
                added += 1
            self._store[key][member] = score
            self._store[key] = self._store[key]
        return added

    @overload
    def zrange(
        self, key: str, start: int, end: int, withscores: Literal[True]
    ) -> list[tuple[str, int]]: ...

    @overload
    def zrange(
        self, key: str, start: int, end: int, withscores: Literal[False]
    ) -> list[str]: ...

    @overload
    def zrange(self, key: str, start: int, end: int) -> list[str]: ...

    def zrange(
        self, key: str, start: int, end: int, withscores: bool = False
    ) -> list[tuple[str, int]] | list[str]:
        if key not in self._store or not isinstance(self._store[key], dict):
            return []
        sorted_items = sorted(
            self._store[key].items(), key=lambda item: item[1]
        )
        if end == -1:
            end = len(sorted_items)
        else:
            end += 1
        return (
            sorted_items[start:end]
            if withscores
            else [k for k, _ in sorted_items[start:end]]
        )
