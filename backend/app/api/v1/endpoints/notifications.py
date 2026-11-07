from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.support import Notification
from app.models.user import User
from app.schemas.support import NotificationOut
from app.schemas.common import APIResponse
from app.services.notification_service import NotificationService
from app.utils.websocket_manager import ws_manager
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=APIResponse[List[NotificationOut]])
def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all notifications for the authenticated user."""
    notifs = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return APIResponse(
        success=True,
        message="Notifications retrieved",
        data=[NotificationOut.model_validate(n) for n in notifs]
    )


@router.put("/{notification_id}/read", response_model=APIResponse[NotificationOut])
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marks a notification as read."""
    notif = NotificationService.mark_as_read(db=db, notification_id=notification_id, user_id=current_user.id)
    if not notif:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return APIResponse(
        success=True,
        message="Notification marked as read",
        data=NotificationOut.model_validate(notif)
    )


@router.websocket("/ws/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: int):
    """WebSocket channel for live notifications and alerts."""
    await ws_manager.connect(user_id=user_id, websocket=websocket)
    try:
        while True:
            # Keep-alive ping/pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id=user_id, websocket=websocket)
