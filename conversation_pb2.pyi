from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConversationRequest(_message.Message):
    __slots__ = ("conversationID", "fileName", "file")
    CONVERSATIONID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    conversationID: str
    fileName: str
    file: bytes
    def __init__(self, conversationID: _Optional[str] = ..., fileName: _Optional[str] = ..., file: _Optional[bytes] = ...) -> None: ...

class ConversationReply(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
