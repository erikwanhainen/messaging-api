from sqlmodel import Session
from typing import List
from uuid import UUID

from app.schemas import MessageCreate
from app.repositories import messages as repo
from app.enums import SortOrder
from app.models import Message


def send_message(session: Session, data: MessageCreate) -> Message:
    return repo.create_message(session, data)


def fetch_unread(
    session: Session,
    recipient: str,
    offset: int,
    limit: int,
    order: SortOrder = SortOrder.desc,
) -> List[Message]:
    return repo.get_unread_messages_by_recipient(
        session, recipient, offset=offset, limit=limit, order=order
    )


def mark_messages_as_read_by_ids(session: Session, message_ids: List[UUID]):
    repo.mark_messages_as_read_by_ids(session, message_ids)


def fetch_messages(
    session: Session,
    recipient: str,
    offset: int,
    limit: int,
    order: SortOrder = SortOrder.desc,
) -> List[Message]:
    return repo.get_messages_by_recipient(
        session, recipient, offset=offset, limit=limit, order=order
    )


def remove_message(session: Session, message_id):
    repo.delete_message(session, message_id)


def remove_multiple_messages(session: Session, ids: list):
    repo.delete_messages(session, ids)
