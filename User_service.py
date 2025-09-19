from models import UserAlertPreference, now_utc
from repo import repo

class UserService:
    def get_or_create_pref(self, user_id: str, alert_id: str) -> UserAlertPreference:
        key = f"{user_id}:{alert_id}"
        pref = repo.user_prefs.get(key)
        if not pref:
            pref = UserAlertPreference(user_id=user_id, alert_id=alert_id)
            repo.user_prefs[key] = pref
        return pref

    def snooze(self, user_id: str, alert_id: str):
        pref = self.get_or_create_pref(user_id, alert_id)
        pref.snoozed_until = now_utc().date()
        return pref

    def mark_read(self, user_id: str, alert_id: str, read: bool):
        pref = self.get_or_create_pref(user_id, alert_id)
        pref.read = read
        return pref
