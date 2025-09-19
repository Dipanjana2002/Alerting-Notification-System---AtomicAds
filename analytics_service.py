from typing import Dict, Any
from models import Severity, now_utc
from repo import repo
from services.delivery_service import DeliveryService
from services.user_service import UserService

class AnalyticsService:
    def summary(self) -> Dict[str, Any]:
        total_alerts = len(repo.alerts)
        delivered = len(repo.notifications)
        read_count = sum(1 for nd in repo.notifications
                         if repo.user_prefs.get(f"{nd.user_id}:{nd.alert_id}") and
                         repo.user_prefs[f"{nd.user_id}:{nd.alert_id}"].read)
        snoozed_counts = {}
        pending_counts = {}
        severity_count = {s.value: 0 for s in Severity}
        for a in repo.alerts.values():
            severity_count[a.severity.value] += 1
            audience = DeliveryService().resolve_audience(a)
            pending = 0
            for u in audience:
                pref = UserService().get_or_create_pref(u.id, a.id)
                if not pref.is_snoozed_today(now_utc()) and not pref.delivered_today(now_utc()):
                    pending += 1
            pending_counts[a.id] = pending
        for pref in repo.user_prefs.values():
            if pref.snoozed_until:
                snoozed_counts[pref.alert_id] = snoozed_counts.get(pref.alert_id, 0) + 1
        return {
            "total_alerts": total_alerts,
            "delivered_notifications_total": delivered,
            "delivered_and_read": read_count,
            "snoozed_counts_per_alert": snoozed_counts,
            "pending_notifications_per_alert": pending_counts,
            "by_severity": severity_count
        }
