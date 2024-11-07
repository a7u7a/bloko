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
    def __init__(self, scroller):
        super().__init__(
            patterns=['*.json'],
            ignore_directories=True,
            case_sensitive=False
        )
        self.scroller = scroller
  
    def on_created(self, event):
        logging.info(f"Watchdog received created event - {event.src_path}")
        
    def on_modified(self, event):
        logging.info(f"Watchdog received modified event - {event.src_path}")
        self.scroller.load_stocks()
  
class JsonWatcher:
    def __init__(self, data_dir, scroller):
        self.event_handler = Handler(scroller)
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(
            self.event_handler,
            path=data_dir,
            recursive=False
        )
        self.observer.daemon = True

    def start(self):
        logging.info("Starting JSON file watcher")
        self.observer.start()

    def stop(self):
        logging.info("Stopping JSON file watcher")
        self.observer.stop()
        self.observer.join()

def main():
    logging.info("Initializing scroller application")
    
    # Initialize scroller
    scroller = Scroller()
    if not scroller.process():
        scroller.print_help()
        return

    # Initialize and start file watcher
    data_dir = os.path.dirname(DATA_FILE_PATH)
    json_watcher = JsonWatcher(data_dir, scroller)
    json_watcher.start()

if __name__ == "__main__":
    main()