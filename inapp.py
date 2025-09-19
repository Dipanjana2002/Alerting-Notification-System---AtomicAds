import uuid
from models import Alert, User, NotificationDelivery
from repo import repo
from .base import DeliveryStrategy

class InAppDeliveryStrategy(DeliveryStrategy):
    def deliver(self, alert: Alert, user: User) -> NotificationDelivery:
        nd = NotificationDelivery(
            id=str(uuid.uuid4()), alert_id=alert.id, user_id=user.id
        )
        repo.notifications.append(nd)
        return nd
