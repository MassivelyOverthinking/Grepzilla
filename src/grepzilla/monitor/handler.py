#========================================================================================================================
# IMPORTS & MODULES
#========================================================================================================================

from time import time

from watchdog.events import FileSystemEventHandler

#========================================================================================================================
# WATCHDOG FILE HANDLER
#========================================================================================================================

class DebouncingFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_event_time = {}

    def on_created(self, event):
        if event.is_directory:
            return
        now = time.time()
        if event.src_path not in self.last_event_time or now - self.last_event_time[event.src_path] > 1:
            print(f"Debounced Created: {event.src_path}")
            self.last_event_time[event.src_path] = now

    def on_modified(self, event):
        if event.is_directory:
            return
        now = time.time()
        if event.src_path not in self.last_event_time or now - self.last_event_time[event.src_path] > 1:
            print(f"Debounced Modified: {event.src_path}")
            self.last_event_time[event.src_path] = now

    def on_deleted(self, event):
        if event.is_directory:
            return
        now = time.time()
        if event.src_path not in self.last_event_time or now - self.last_event_time[event.src_path] > 1:
            print(f"Debounced Deleted: {event.src_path}")
            self.last_event_time[event.src_path] = now