import uuid
from datetime import datetime
from typing import List, Optional
from models import Alert, Severity
from repo import repo
from models import now_utc

class AlertService:
    def create_alert(self, **data) -> Alert:
        aid = str(uuid.uuid4())
        alert = Alert(id=aid, **data)
        repo.alerts[aid] = alert
        return alert

    def update_alert(self, alert_id: str, **patch) -> Alert:
        alert = repo.alerts.get(alert_id)
        if not alert:
            raise KeyError("Alert not found")
        for k, v in patch.items():
            if hasattr(alert, k):
                setattr(alert, k, v)
        alert.updated_at = now_utc()
        return alert

    def list_alerts(self, severity: Optional[Severity] = None, active: Optional[bool] = None) -> List[Alert]:
        ref = now_utc()
        result = []
        for a in repo.alerts.values():
            if severity and a.severity != severity:
                continue
            if active is not None:
                if active and not self.is_active(a, ref):
                    continue
                if not active and self.is_active(a, ref):
                    continue
            result.append(a)
        return result

    def is_active(self, alert: Alert, ref: datetime) -> bool:
        if alert.archived: return False
        if alert.start_at and ref < alert.start_at: return False
        if alert.expires_at and ref >= alert.expires_at: return False
        return True
