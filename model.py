from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

def now_utc():
    return datetime.now(timezone.utc)

class Severity(str, Enum):
    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"

class DeliveryType(str, Enum):
    IN_APP = "in_app"

class User(BaseModel):
    id: str
    name: str
    team_id: Optional[str]

class Team(BaseModel):
    id: str
    name: str

class Alert(BaseModel):
    id: str
    title: str
    body: str
    severity: Severity
    delivery_type: DeliveryType = DeliveryType.IN_APP
    reminder_enabled: bool = True
    start_at: datetime = Field(default_factory=now_utc)
    expires_at: Optional[datetime] = None
    visibility_org: bool = False
    visibility_team_ids: List[str] = []
    visibility_user_ids: List[str] = []
    archived: bool = False
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

class NotificationDelivery(BaseModel):
    id: str
    alert_id: str
    user_id: str
    delivered_at: datetime = Field(default_factory=now_utc)

class UserAlertPreference(BaseModel):
    user_id: str
    alert_id: str
    read: bool = False
    snoozed_until: Optional[datetime.date] = None
    last_delivered: Optional[datetime] = None

    def is_snoozed_today(self, reference_dt: datetime) -> bool:
        return self.snoozed_until == reference_dt.date()

    def delivered_today(self, reference_dt: datetime) -> bool:
        return self.last_delivered and self.last_delivered.date() == reference_dt.date()
