from ipaddress import IPv4Address
from typing import Annotated, Literal

import grpc
from pydantic import AfterValidator, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from random_word.random_word import RandomWords

from cluster.proto_py import datastore_pb2, datastore_pb2_grpc


def get_group(length: int) -> str:
    r = RandomWords()
    return '-'.join(r.get_random_word() for _ in range(length))


class NodeSettings(BaseSettings):
    address: Annotated[str, AfterValidator(lambda ip: IPv4Address(ip))]
    port: Annotated[int, Field(strict=True, ge=0, le=65535)]
    role: Literal['replica', 'shard']
    group: str = get_group(5)

    @computed_field
    @property
    def socket(self) -> str:
        return str(self.address) + ':' + str(self.port)

    model_config = SettingsConfigDict()


class Node:
    def __init__(self, settings: NodeSettings) -> None:
        self.settings = settings
        self.channel = grpc.aio.insecure_channel(settings.socket)
        self.ds = datastore_pb2_grpc.DatastoreServiceStub(self.channel)

    async def disconnect(self):
        await self.channel.close()


class Manager:
    def __init__(self) -> None:
        self._nodes: list[Node] = []

    def add_node(self, node: Node):
        self._nodes.append(node)

    def _get_node(self):
        return self._nodes[0]

    async def strset(self, key: str, value: str) -> bool:
        node = self._get_node()
        result: datastore_pb2.BoolReply = await node.ds.StrSet(
            datastore_pb2.KeyValue(key=key, value=value)
        )
        return result.result

    async def strget(self, key: str) -> str:
        node = self._get_node()
        result: datastore_pb2.StringReply = await node.ds.StrGet(
            datastore_pb2.Key(key=key)
        )
        return result.result
