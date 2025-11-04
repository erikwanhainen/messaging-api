from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List


class MessageCreate(BaseModel):
    recipient: str = Field(
        description="Identifier of the recipient (cannot be empty or only whitespace)",
        examples=["user@example.com"],
    )
    content: str = Field(
        description="Plain text message content (cannot be empty or only whitespace)",
        examples=["Hello Sir"],
    )

    @field_validator("recipient")
    @classmethod
    def recipient_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Recipient cannot be empty or only whitespace")
        return v

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message content cannot be empty or only whitespace")
        return v


class MessageRead(BaseModel):
    id: UUID
    recipient: str
    content: str
    created_at: datetime
    read: bool


class MessageMarkReadRequest(BaseModel):
    message_ids: List[UUID]


class MessageBulkDeleteRequest(BaseModel):
    message_ids: List[UUID]
