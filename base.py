from abc import ABC, abstractmethod
from models import Alert, User, NotificationDelivery

class DeliveryStrategy(ABC):
    @abstractmethod
    def deliver(self, alert: Alert, user: User) -> NotificationDelivery:
        pass
