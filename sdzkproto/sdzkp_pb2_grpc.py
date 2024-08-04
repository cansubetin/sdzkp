# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from sdzkproto import sdzkp_pb2 as sdzkproto_dot_sdzkp__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in sdzkproto/sdzkp_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class SDZKPStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Setup = channel.unary_unary(
                '/sdzkp.SDZKP/Setup',
                request_serializer=sdzkproto_dot_sdzkp__pb2.SGDInstance.SerializeToString,
                response_deserializer=sdzkproto_dot_sdzkp__pb2.SetupAck.FromString,
                _registered_method=True)
        self.Commit = channel.unary_unary(
                '/sdzkp.SDZKP/Commit',
                request_serializer=sdzkproto_dot_sdzkp__pb2.Commitments.SerializeToString,
                response_deserializer=sdzkproto_dot_sdzkp__pb2.Challenge.FromString,
                _registered_method=True)
        self.Verify = channel.unary_unary(
                '/sdzkp.SDZKP/Verify',
                request_serializer=sdzkproto_dot_sdzkp__pb2.Response.SerializeToString,
                response_deserializer=sdzkproto_dot_sdzkp__pb2.VerificationResult.FromString,
                _registered_method=True)


class SDZKPServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Setup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Commit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Verify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SDZKPServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Setup': grpc.unary_unary_rpc_method_handler(
                    servicer.Setup,
                    request_deserializer=sdzkproto_dot_sdzkp__pb2.SGDInstance.FromString,
                    response_serializer=sdzkproto_dot_sdzkp__pb2.SetupAck.SerializeToString,
            ),
            'Commit': grpc.unary_unary_rpc_method_handler(
                    servicer.Commit,
                    request_deserializer=sdzkproto_dot_sdzkp__pb2.Commitments.FromString,
                    response_serializer=sdzkproto_dot_sdzkp__pb2.Challenge.SerializeToString,
            ),
            'Verify': grpc.unary_unary_rpc_method_handler(
                    servicer.Verify,
                    request_deserializer=sdzkproto_dot_sdzkp__pb2.Response.FromString,
                    response_serializer=sdzkproto_dot_sdzkp__pb2.VerificationResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sdzkp.SDZKP', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('sdzkp.SDZKP', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SDZKP(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Setup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/sdzkp.SDZKP/Setup',
            sdzkproto_dot_sdzkp__pb2.SGDInstance.SerializeToString,
            sdzkproto_dot_sdzkp__pb2.SetupAck.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Commit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/sdzkp.SDZKP/Commit',
            sdzkproto_dot_sdzkp__pb2.Commitments.SerializeToString,
            sdzkproto_dot_sdzkp__pb2.Challenge.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Verify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/sdzkp.SDZKP/Verify',
            sdzkproto_dot_sdzkp__pb2.Response.SerializeToString,
            sdzkproto_dot_sdzkp__pb2.VerificationResult.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)