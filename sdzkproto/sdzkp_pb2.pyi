from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SGDInstance(_message.Message):
    __slots__ = ("sgdid", "g", "n", "m", "generators", "min_distance", "number_of_rounds")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    GENERATORS_FIELD_NUMBER: _ClassVar[int]
    MIN_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_ROUNDS_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    g: _containers.RepeatedScalarFieldContainer[int]
    n: int
    m: int
    generators: _containers.RepeatedScalarFieldContainer[int]
    min_distance: int
    number_of_rounds: int
    def __init__(self, sgdid: _Optional[str] = ..., g: _Optional[_Iterable[int]] = ..., n: _Optional[int] = ..., m: _Optional[int] = ..., generators: _Optional[_Iterable[int]] = ..., min_distance: _Optional[int] = ..., number_of_rounds: _Optional[int] = ...) -> None: ...

class SetupAck(_message.Message):
    __slots__ = ("sgdid", "setupresult")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    SETUPRESULT_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    setupresult: bool
    def __init__(self, sgdid: _Optional[str] = ..., setupresult: bool = ...) -> None: ...

class Commitments(_message.Message):
    __slots__ = ("sgdid", "roundid", "C1", "C2", "C3")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    ROUNDID_FIELD_NUMBER: _ClassVar[int]
    C1_FIELD_NUMBER: _ClassVar[int]
    C2_FIELD_NUMBER: _ClassVar[int]
    C3_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    roundid: int
    C1: bytes
    C2: bytes
    C3: bytes
    def __init__(self, sgdid: _Optional[str] = ..., roundid: _Optional[int] = ..., C1: _Optional[bytes] = ..., C2: _Optional[bytes] = ..., C3: _Optional[bytes] = ...) -> None: ...

class Challenge(_message.Message):
    __slots__ = ("sgdid", "roundid", "challenge")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    ROUNDID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    roundid: int
    challenge: int
    def __init__(self, sgdid: _Optional[str] = ..., roundid: _Optional[int] = ..., challenge: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("sgdid", "roundid", "Z1", "Z2", "s", "t_r", "t_u")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    ROUNDID_FIELD_NUMBER: _ClassVar[int]
    Z1_FIELD_NUMBER: _ClassVar[int]
    Z2_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    T_R_FIELD_NUMBER: _ClassVar[int]
    T_U_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    roundid: int
    Z1: _containers.RepeatedScalarFieldContainer[int]
    Z2: _containers.RepeatedScalarFieldContainer[int]
    s: int
    t_r: _containers.RepeatedScalarFieldContainer[int]
    t_u: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, sgdid: _Optional[str] = ..., roundid: _Optional[int] = ..., Z1: _Optional[_Iterable[int]] = ..., Z2: _Optional[_Iterable[int]] = ..., s: _Optional[int] = ..., t_r: _Optional[_Iterable[int]] = ..., t_u: _Optional[_Iterable[int]] = ...) -> None: ...

class VerificationResult(_message.Message):
    __slots__ = ("sgdid", "roundid", "roundresult", "verificationresult")
    SGDID_FIELD_NUMBER: _ClassVar[int]
    ROUNDID_FIELD_NUMBER: _ClassVar[int]
    ROUNDRESULT_FIELD_NUMBER: _ClassVar[int]
    VERIFICATIONRESULT_FIELD_NUMBER: _ClassVar[int]
    sgdid: str
    roundid: int
    roundresult: bool
    verificationresult: bool
    def __init__(self, sgdid: _Optional[str] = ..., roundid: _Optional[int] = ..., roundresult: bool = ..., verificationresult: bool = ...) -> None: ...
