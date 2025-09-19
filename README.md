# Alerting-Notification-System---AtomicAds

This is a lightweight Alerting & Notification Platform built with FastAPI, designed to:
a. Deliver timely alerts to users based on visibility and severity.
b. Support in-app reminders with snooze/read/unread tracking.
c. Provide analytics for delivered, read, snoozed, and pending notifications.
d. The system is fully OOP-based, modular, and extensible for new delivery channels (e.g., email, SMS).

Features:-

Alert Management (CRUD):
 Create, update, and list alerts
 Control visibility: organization-wide, team-specific, or individual users

Notification Delivery:
 In-app delivery strategy implemented
 Modular Strategy Pattern for easy addition of new delivery channels

User Preferences:
 Snooze alerts for a day
 Mark alerts as read/unread
 State management for reminders

Reminders:
 Configurable scheduler (default 2h interval)
 Manual trigger via API for demo purposes

Analytics:
 Aggregated alert data per severity, delivery, snooze, and pending notifications

Seed Data:
 Predefined users and teams for testing visibility

Design Principles:-

 OOP & SRP: Services and models separated for maintainability.

 Strategy Pattern: Notification channels decoupled from core logic.

 State Management: Snooze/read/unread logic encapsulated in UserAlertPreference.

 Separation of Concerns:

  AlertService - Alert CRUD & visibility
  DeliveryService - Delivery & reminders
  UserService - Preferences & state
  AnalyticsService - Aggregated metrics
Seed Data

Predefined users and teams for testing visibility
