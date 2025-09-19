import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from models import Alert, Severity, DeliveryType
from services import AlertService, DeliveryService, UserService, AnalyticsService
from scheduler import ReminderScheduler
from repository import repo, now_utc

# Services & Scheduler-
alert_service = AlertService()
delivery_service = DeliveryService()
user_service = UserService()
analytics_service = AnalyticsService()
scheduler = ReminderScheduler(delivery_service)

# FastAPI app
app = FastAPI(title="Alerting & Notification MVP (PRD-compliant)")

# DTOs
class AlertCreateDTO(BaseModel):
    title: str
    body: str
    severity: Severity = Severity.INFO
    delivery_type: DeliveryType = DeliveryType.IN_APP
    reminder_enabled: bool = True
    start_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    visibility_org: bool = False
    visibility_team_ids: List[str] = []
    visibility_user_ids: List[str] = []

class AlertUpdateDTO(BaseModel):
    title: Optional[str]
    body: Optional[str]
    severity: Optional[Severity]
    reminder_enabled: Optional[bool]
    start_at: Optional[datetime]
    expires_at: Optional[datetime]
    visibility_org: Optional[bool]
    visibility_team_ids: Optional[List[str]]
    visibility_user_ids: Optional[List[str]]
    archived: Optional[bool]

class SnoozeRequest(BaseModel):
    user_id: str
    alert_id: str

class ReadToggleRequest(BaseModel):
    user_id: str
    alert_id: str
    read: bool

# Admin Endpoints
@app.post("/admin/alerts", response_model=Alert)
def create_alert(payload: AlertCreateDTO):
    return alert_service.create_alert(
        title=payload.title,
        body=payload.body,
        severity=payload.severity,
        delivery_type=payload.delivery_type,
        reminder_enabled=payload.reminder_enabled,
        start_at=payload.start_at or now_utc(),
        expires_at=payload.expires_at,
        visibility_org=payload.visibility_org,
        visibility_team_ids=payload.visibility_team_ids,
        visibility_user_ids=payload.visibility_user_ids
    )

@app.patch("/admin/alerts/{alert_id}", response_model=Alert)
def update_alert(alert_id: str, payload: AlertUpdateDTO):
    try:
        return alert_service.update_alert(alert_id, **payload.dict(exclude_none=True))
    except KeyError:
        raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/admin/alerts", response_model=List[Alert])
def list_alerts(severity: Optional[Severity] = None, active: Optional[bool] = None):
    return alert_service.list_alerts(severity=severity, active=active)

@app.post("/admin/trigger-reminders")
def trigger_reminders():
    return delivery_service.run_reminder_pass()

@app.get("/admin/analytics")
def analytics():
    return analytics_service.summary()

# User Endpoints

@app.get("/user/{user_id}/alerts")
def get_user_alerts(user_id: str):
    if user_id not in repo.users:
        raise HTTPException(404, "User not found")

    ref = now_utc()
    res = []
    for a in repo.alerts.values():
        if not alert_service.is_active(a, ref):
            continue
        audience = delivery_service.resolve_audience(a)
        if any(u.id == user_id for u in audience):
            pref = user_service.get_or_create_pref(user_id, a.id)
            res.append({"alert": a, "preference": pref})
    return {"user": repo.users[user_id], "alerts": res}

@app.post("/user/mark-read")
def mark_read(payload: ReadToggleRequest):
    if payload.user_id not in repo.users:
        raise HTTPException(404, "User not found")
    if payload.alert_id not in repo.alerts:
        raise HTTPException(404, "Alert not found")
    pref = user_service.mark_read(payload.user_id, payload.alert_id, payload.read)
    return {"status": "ok", "preference": pref}

@app.post("/user/snooze")
def snooze_alert(payload: SnoozeRequest):
    if payload.user_id not in repo.users:
        raise HTTPException(404, "User not found")
    if payload.alert_id not in repo.alerts:
        raise HTTPException(404, "Alert not found")
    pref = user_service.snooze(payload.user_id, payload.alert_id)
    return {"status": "snoozed_for_today", "preference": pref}

@app.get("/user/{user_id}/snoozed")
def get_snoozed(user_id: str):
    if user_id not in repo.users:
        raise HTTPException(404, "User not found")
    res = [
        p for p in repo.user_prefs.values()
        if p.user_id == user_id and p.snoozed_until is not None
    ]
    return {"snoozed": res}

# Metadata Endpoints
@app.get("/meta/users")
def list_users():
    return list(repo.users.values())

@app.get("/meta/teams")
def list_teams():
    return list(repo.teams.values())

# Scheduler Control-
@app.post("/admin/scheduler/start")
def start_scheduler(interval_seconds: Optional[int] = None):
    scheduler.start(interval_seconds=interval_seconds)
    return {"status": "started", "interval_seconds": scheduler.interval_seconds}

@app.post("/admin/scheduler/stop")
def stop_scheduler():
    scheduler.stop()
    return {"status": "stopped"}

# To run the server
if __name__ == "__main__":
    scheduler.start(interval_seconds=60) 
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
