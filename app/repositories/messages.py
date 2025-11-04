from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from app.models import Message
from app.schemas import MessageCreate
from app.enums import SortOrder


def create_message(session: Session, data: MessageCreate) -> Message:
    msg = Message(**data.dict())
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


def get_messages_by_recipient(
    session: Session,
    recipient: str,
    offset: int = 0,
    limit: Optional[int] = None,
    order: SortOrder = SortOrder.desc,
) -> List[Message]:
    query = select(Message).where(Message.recipient == recipient)

    if order == SortOrder.desc:
        query = query.order_by(Message.created_at.desc())
    else:
        query = query.order_by(Message.created_at.asc())

    if limit is not None:
        query = query.offset(offset).limit(limit)

    return session.exec(query).all()


def get_unread_messages_by_recipient(
    session: Session,
    recipient: str,
    offset: int = 0,
    limit: Optional[int] = None,
    order: SortOrder = SortOrder.desc,
) -> List[Message]:
    query = select(Message).where(Message.recipient == recipient, Message.read == False)

    if order == SortOrder.desc:
        query = query.order_by(Message.created_at.desc())
    else:
        query = query.order_by(Message.created_at.asc())

    if limit is not None:
        query = query.offset(offset).limit(limit)

    return session.exec(query).all()


def mark_messages_as_read(session: Session, messages: List[Message]):
    for msg in messages:
        msg.read = True
    session.commit()


def mark_messages_as_read_by_ids(session: Session, message_ids: List[UUID]):
    messages = session.exec(select(Message).where(Message.id.in_(message_ids))).all()
    for msg in messages:
        msg.read = True
    session.commit()


def delete_message(session: Session, message_id):
    msg = session.get(Message, message_id)
    if msg:
        session.delete(msg)
        session.commit()


def delete_messages(session: Session, ids: list):
    for mid in ids:
        msg = session.get(Message, mid)
        if msg:
            session.delete(msg)
    session.commit()
