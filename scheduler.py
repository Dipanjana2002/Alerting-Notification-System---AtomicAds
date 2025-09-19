import threading
from services.delivery_service import DeliveryService

class ReminderScheduler:
    def __init__(self, delivery_service: DeliveryService):
        self.delivery_service = delivery_service
        self._thread = None
        self._stop_event = threading.Event()
        self.interval_seconds = 2 * 3600

    def _loop(self):
        while not self._stop_event.is_set():
            try:
                result = self.delivery_service.run_reminder_pass()
                if result["sent_count"] > 0:
                    print(f"[ReminderScheduler] Sent {result['sent_count']} notifications at {result['reference']}")
            except Exception as e:
                print("Scheduler error:", e)
            if self._stop_event.wait(self.interval_seconds):
                break

    def start(self, interval_seconds: int = None):
        if interval_seconds: self.interval_seconds = interval_seconds
        if self._thread and self._thread.is_alive(): return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"ReminderScheduler started (interval_seconds={self.interval_seconds})")

    def stop(self):
        self._stop_event.set()
        if self._thread: self._thread.join(timeout=1)
        print("ReminderScheduler stopped")
