import time
import threading
from collections import deque

try:
    import pygetwindow as gw
    WINDOW_TRACKING = True
except:
    WINDOW_TRACKING = False

class TabMonitor:
    def __init__(self):
        self.switches = deque(maxlen=200)
        self.last_window = ""
        self.running = True
        self.study_apps = ["chrome", "edge", "firefox", "notepad", "code", "word", "pdf"]
        self.distraction_apps = ["youtube", "instagram", "facebook", "twitter", "tiktok", "discord", "whatsapp"]
        self.current_app = "unknown"
        self.is_distracted = False

        if WINDOW_TRACKING:
            thread = threading.Thread(target=self._monitor_loop, daemon=True)
            thread.start()

    def _monitor_loop(self):
        while self.running:
            try:
                win = gw.getActiveWindow()
                if win and win.title:
                    title = win.title.lower()
                    if title != self.last_window:
                        if self.last_window != "":
                            self.switches.append(time.time())
                        self.last_window = title
                        self.current_app = title

                        # Check if distraction
                        self.is_distracted = any(
                            app in title for app in self.distraction_apps
                        )
            except:
                pass
            time.sleep(0.5)

    def switches_per_hour(self):
        now = time.time()
        recent = [t for t in self.switches if now - t < 3600]
        return len(recent)

    def switches_last_5min(self):
        now = time.time()
        recent = [t for t in self.switches if now - t < 300]
        return len(recent)

    def get_status(self):
        sph = self.switches_per_hour()
        if self.is_distracted:
            return "DISTRACTED"
        elif sph > 20:
            return "HIGH SWITCHING"
        elif sph > 10:
            return "MODERATE"
        else:
            return "FOCUSED"