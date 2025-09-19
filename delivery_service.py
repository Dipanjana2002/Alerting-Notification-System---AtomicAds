from typing import List, Dict, Any, Optional
from models import Alert, User, DeliveryType, now_utc
from repo import repo
from services.alert_service import AlertService
from services.user_service import UserService
from delivery.inapp import InAppDeliveryStrategy

class DeliveryService:
    def __init__(self):
        self.strategies = {DeliveryType.IN_APP: InAppDeliveryStrategy()}

    def resolve_audience(self, alert: Alert) -> List[User]:
        users_set = {}
        if alert.visibility_org:
            return list(repo.users.values())
        for uid in alert.visibility_user_ids:
            u = repo.users.get(uid)
            if u: users_set[u.id] = u
        for tid in alert.visibility_team_ids:
            for u in repo.users.values():
                if u.team_id == tid:
                    users_set[u.id] = u
        return list(users_set.values())

    def run_reminder_pass(self, reference_dt: Optional[str] = None) -> Dict[str, Any]:
        ref = reference_dt or now_utc()
        sent = []
        skipped = []
        for alert in repo.alerts.values():
            if not alert.reminder_enabled or not AlertService().is_active(alert, ref):
                continue
            audience = self.resolve_audience(alert)
            for user in audience:
                pref = UserService().get_or_create_pref(user.id, alert.id)
                if pref.is_snoozed_today(ref) or pref.delivered_today(ref):
                    skipped.append({"alert_id": alert.id, "user_id": user.id})
                    continue
                strategy = self.strategies.get(alert.delivery_type)
                if not strategy: continue
                nd = strategy.deliver(alert, user)
                pref.last_delivered = now_utc()
                sent.append({"notification_id": nd.id, "alert_id": alert.id, "user_id": user.id})
        return {"reference": ref.isoformat(), "sent_count": len(sent), "sent": sent, "skipped": skipped}
