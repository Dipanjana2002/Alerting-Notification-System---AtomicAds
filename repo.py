from typing import Dict, List
from models import User, Team, Alert, NotificationDelivery, UserAlertPreference

class InMemoryRepo:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.teams: Dict[str, Team] = {}
        self.alerts: Dict[str, Alert] = {}
        self.notifications: List[NotificationDelivery] = []
        self.user_prefs: Dict[str, UserAlertPreference] = {}

repo = InMemoryRepo()
