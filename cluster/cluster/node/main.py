from __future__ import annotations

import asyncio
import signal
from typing import Annotated

import grpc
from pydantic import AfterValidator, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ipaddress import IPv4Address

from cluster.proto_py import datastore_pb2, datastore_pb2_grpc

from .datastore import Datastore


class DatastoreService(datastore_pb2_grpc.DatastoreServiceServicer):
    def __init__(self, node: Node) -> None:
        super().__init__()
        self.node = node

    def StrSet(self, request: datastore_pb2.KeyValue, context):
        return datastore_pb2.IntReply(
            result=node.ds.strset(request.key, request.value)
        )

    def StrGet(self, request: datastore_pb2.Key, context):
        return datastore_pb2.StringReply(result=node.ds.strget(request.key))


class NodeSettings(BaseSettings):
    address: Annotated[str, AfterValidator(lambda ip: IPv4Address(ip))]
    port: Annotated[int, Field(strict=True, ge=0, le=65535)]

    @computed_field
    @property
    def socket(self) -> str:
        return str(self.address) + ':' + str(self.port)

    model_config = SettingsConfigDict()


class Node:
    def __init__(self, settings: NodeSettings) -> None:
        self.settings = settings
        self.ds = Datastore()
        self.service = DatastoreService(self)
        self.grpc_server: grpc.aio.Server | None = None

    async def serve(self):
        server = self.grpc_server = grpc.aio.server()
        self.grpc_server.add_insecure_port(self.settings.socket)

        datastore_pb2_grpc.add_DatastoreServiceServicer_to_server(
            self.service, server
        )

        shutdown_event = asyncio.Event()

        def signal_handler():
            print('Received shutdown signal...')
            shutdown_event.set()

        asyncio.get_event_loop().add_signal_handler(
            signal.SIGINT, signal_handler
        )

        await server.start()
        print('Server started, listening on ' + self.settings.socket)

        await shutdown_event.wait()

        print('Stopping server...')
        await server.stop(grace=None)
        print('Server stopped!')


if __name__ == '__main__':
    node_settings = NodeSettings(address='0.0.0.0', port=9063)
    node = Node(settings=node_settings)

    asyncio.run(node.serve())
