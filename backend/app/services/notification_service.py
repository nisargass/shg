import asyncio
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.support import Notification
from app.utils.websocket_manager import ws_manager


class NotificationService:

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notif_type: str,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notif_type,
            reference_id=reference_id,
            reference_type=reference_type,
            is_read=False
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)

        # Dispatch async to WebSocket connection if active
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(
                    ws_manager.send_personal_message(
                        {
                            "id": notif.id,
                            "title": notif.title,
                            "message": notif.message,
                            "notification_type": notif.notification_type,
                            "reference_id": notif.reference_id,
                            "created_at": notif.created_at.isoformat()
                        },
                        user_id=user_id
                    )
                )
        except Exception:
            pass

        return notif

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
        notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if notif:
            notif.is_read = True
            db.commit()
            db.refresh(notif)
        return notif
