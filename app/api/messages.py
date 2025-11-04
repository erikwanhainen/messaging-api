from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.schemas import (
    MessageCreate,
    MessageRead,
    MessageMarkReadRequest,
    MessageBulkDeleteRequest,
)
from app.services import messages as service
from app.db import get_session
from app.enums import SortOrder
from app.config import MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE


router = APIRouter(prefix="/messages")


@router.post("/", response_model=MessageRead)
def send_message_endpoint(data: MessageCreate, session: Session = Depends(get_session)):
    """Send a new message to a recipient."""
    return service.send_message(session, data)


@router.get("/unread/", response_model=List[MessageRead])
def get_unread_endpoint(
    recipient: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    order: SortOrder = Query(SortOrder.desc),
    session: Session = Depends(get_session),
):
    """
    Retrieve unread messages for a recipient with pagination and sorting.
    Does not mark messages as read.
    """
    return service.fetch_unread(session, recipient, offset, limit, order)


@router.patch("/mark-read", status_code=204)
def mark_read_endpoint(
    data: MessageMarkReadRequest, session: Session = Depends(get_session)
):
    """Mark messages as read (idempotent)."""
    service.mark_messages_as_read_by_ids(session, data.message_ids)


@router.get("/", response_model=List[MessageRead])
def get_messages_endpoint(
    recipient: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    order: SortOrder = Query(SortOrder.desc),
    session: Session = Depends(get_session),
):
    """Retrieve messages for a recipient with pagination and sorting."""
    return service.fetch_messages(session, recipient, offset, limit, order)


@router.delete("/bulk", status_code=204)
def delete_multiple_endpoint(
    data: MessageBulkDeleteRequest, session: Session = Depends(get_session)
):
    """Delete multiple messages (idempotent)."""
    service.remove_multiple_messages(session, data.message_ids)


@router.delete("/{message_id}", status_code=204)
def delete_message_endpoint(message_id: UUID, session: Session = Depends(get_session)):
    """Delete a single message (idempotent)."""
    service.remove_message(session, message_id)
