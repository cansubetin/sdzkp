rm -rf protogen
python -m grpc_tools.protoc -Isdzkproto=./api --python_out=. --pyi_out=. --grpc_python_out=. ./api/sdzkp.proto 