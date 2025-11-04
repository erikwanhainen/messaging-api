from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4, UUID


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    recipient: str = Field(max_length=255, index=True, nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    read: bool = Field(default=False, index=True, nullable=False)
