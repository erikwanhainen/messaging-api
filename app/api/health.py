from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    """Health check. Verifies database connection."""
    try:
        session.exec(select(1)).first()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "database": "disconnected", "error": str(e)},
        )
