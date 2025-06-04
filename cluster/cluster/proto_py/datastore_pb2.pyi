from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Key(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KeyMultiValue(_message.Message):
    __slots__ = ("key", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class RangeRequest(_message.Message):
    __slots__ = ("key", "start", "end")
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    key: str
    start: int
    end: int
    def __init__(self, key: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class BoolReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class IntReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class StringReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class StringListReply(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, results: _Optional[_Iterable[str]] = ...) -> None: ...

class StringSetReply(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, results: _Optional[_Iterable[str]] = ...) -> None: ...

class HashField(_message.Message):
    __slots__ = ("key", "field")
    KEY_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    key: str
    field: str
    def __init__(self, key: _Optional[str] = ..., field: _Optional[str] = ...) -> None: ...

class HSetEntry(_message.Message):
    __slots__ = ("field", "value")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    field: str
    value: str
    def __init__(self, field: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class HSetRequest(_message.Message):
    __slots__ = ("key", "field", "value", "mapping")
    KEY_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MAPPING_FIELD_NUMBER: _ClassVar[int]
    key: str
    field: str
    value: str
    mapping: _containers.RepeatedCompositeFieldContainer[HSetEntry]
    def __init__(self, key: _Optional[str] = ..., field: _Optional[str] = ..., value: _Optional[str] = ..., mapping: _Optional[_Iterable[_Union[HSetEntry, _Mapping]]] = ...) -> None: ...

class HashMapReply(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[HSetEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[HSetEntry, _Mapping]]] = ...) -> None: ...

class ZAddEntry(_message.Message):
    __slots__ = ("member", "score")
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    member: str
    score: float
    def __init__(self, member: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class ZAddRequest(_message.Message):
    __slots__ = ("key", "entries")
    KEY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    key: str
    entries: _containers.RepeatedCompositeFieldContainer[ZAddEntry]
    def __init__(self, key: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[ZAddEntry, _Mapping]]] = ...) -> None: ...

class ZRangeRequest(_message.Message):
    __slots__ = ("key", "start", "end", "withscores")
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    WITHSCORES_FIELD_NUMBER: _ClassVar[int]
    key: str
    start: int
    end: int
    withscores: bool
    def __init__(self, key: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., withscores: bool = ...) -> None: ...

class ZItem(_message.Message):
    __slots__ = ("member", "score")
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    member: str
    score: float
    def __init__(self, member: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class ZRangeReply(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[ZItem]
    def __init__(self, items: _Optional[_Iterable[_Union[ZItem, _Mapping]]] = ...) -> None: ...
