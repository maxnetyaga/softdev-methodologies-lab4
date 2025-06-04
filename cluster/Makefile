.PHONY: test, protocols, start-node, start-manager

export PYTHONPATH:=$(PYTHONPATH):./cluster/proto_py

test:
	uv run pytest -s .

unit-test:
	uv run pytest -m "not integtest" .

integ-test:
	uv run pytest -m "integtest" .

protocols:
	rm -rf cluster/proto_py && mkdir cluster/proto_py && uv run python -m grpc_tools.protoc -I cluster/proto/ --python_out=cluster/proto_py/ --pyi_out=cluster/proto_py/ --grpc_python_out=cluster/proto_py/ cluster/proto/*.proto

start-node:
	uv run -m cluster.node.main

start-manager:
	uv run fastapi run ./cluster/manager/main.py