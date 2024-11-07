import time
import os
import logging
from scrollerbase import Scroller
import watchdog.events
import watchdog.observers

# Project paths setup
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'stocks-data.json')
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'bloko-scroller.log')

# Setup logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(
            patterns=['*.json'],
            ignore_directories=True,
            case_sensitive=False
        )
  
    def on_created(self, event):
        logging.info(f"Watchdog: Stocks file created - {event.src_path}")
        
    def on_modified(self, event):
        logging.info(f"Watchdog: Stocks file modified - {event.src_path}")
        scroller.stock_data.load_stocks()
  
class JsonWatcher:
    def __init__(self, data_dir):
        self.event_handler = Handler()
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(
            self.event_handler,
            path=data_dir,
            recursive=False
        )
        self.observer.daemon = True

    def start(self):
        logging.info("Watchdog: Starting JSON file watcher")
        self.observer.start()

    def stop(self):
        logging.info("Watchdog: Stopping JSON file watcher")
        self.observer.stop()
        self.observer.join()

scroller = Scroller()

data_dir = os.path.dirname(DATA_FILE_PATH)
json_watcher = JsonWatcher(data_dir)
json_watcher.start()
if not scroller.process():
    scroller.print_help()