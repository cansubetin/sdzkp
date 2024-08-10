rm -rf protogen
python -m grpc_tools.protoc -Isdzkp/sdzkproto=./sdzkp/api --python_out=. --pyi_out=. --grpc_python_out=. ./sdzkp/api/sdzkp.proto 