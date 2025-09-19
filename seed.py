from datetime import timedelta
from models import Team, User, Alert, Severity, now_utc
from repo import repo

def seed_demo_data():
    t1 = Team(id="team-eng", name="Engineering")
    t2 = Team(id="team-mkt", name="Marketing")
    repo.teams[t1.id] = t1
    repo.teams[t2.id] = t2

    u1 = User(id="u-alice", name="Alice", team_id="team-eng")
    u2 = User(id="u-bob", name="Bob", team_id="team-eng")
    u3 = User(id="u-carrie", name="Carrie", team_id="team-mkt")
    repo.users[u1.id] = u1
    repo.users[u2.id] = u2
    repo.users[u3.id] = u3

    a1 = Alert(id="alert-1", title="Planned Maintenance", body="Maintenance tonight.",
               severity=Severity.INFO, visibility_org=True,
               start_at=now_utc()-timedelta(hours=1), expires_at=now_utc()+timedelta(days=2))
    a2 = Alert(id="alert-2", title="Security Patch Required", body="Reboot dev boxes.",
               severity=Severity.WARNING, visibility_team_ids=["team-eng"],
               start_at=now_utc()-timedelta(hours=3), expires_at=now_utc()+timedelta(days=1))
    a3 = Alert(id="alert-3", title="Timesheet Reminder", body="Complete timesheet.",
               severity=Severity.INFO, visibility_user_ids=["u-carrie"],
               start_at=now_utc()-timedelta(days=1), expires_at=now_utc()+timedelta(days=7))

    repo.alerts[a1.id] = a1
    repo.alerts[a2.id] = a2
    repo.alerts[a3.id] = a3
