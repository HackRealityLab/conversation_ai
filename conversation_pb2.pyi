from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConversationRequest(_message.Message):
    __slots__ = ("conversationID", "fileName", "file")
    CONVERSATIONID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    conversationID: int
    fileName: str
    file: bytes
    def __init__(self, conversationID: _Optional[int] = ..., fileName: _Optional[str] = ..., file: _Optional[bytes] = ...) -> None: ...

class ConversationReply(_message.Message):
    __slots__ = ("conversationID", "text", "good_percent", "bad_percent")
    CONVERSATIONID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    GOOD_PERCENT_FIELD_NUMBER: _ClassVar[int]
    BAD_PERCENT_FIELD_NUMBER: _ClassVar[int]
    conversationID: int
    text: str
    good_percent: int
    bad_percent: int
    def __init__(self, conversationID: _Optional[int] = ..., text: _Optional[str] = ..., good_percent: _Optional[int] = ..., bad_percent: _Optional[int] = ...) -> None: ...
