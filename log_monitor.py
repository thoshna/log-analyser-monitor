import re
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the path to the log file
LOG_FILE_PATH = 'log_file.txt'

# Regular expression for log pattern to watch for: [2023-04-08 13:00:00] ERROR Something bad happened.
LOG_PATTERN = re.compile(r'\[(.*?)\] (ERROR|WARNING|INFO) (.*)')

# This function will be called when a new log is detected.
def process_new_log_entry(match):
    timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
    log_type = match.group(2)
    message = match.group(3)
    print(f'{timestamp}: {log_type} - {message}')

# This class inherits from FileSystemEventHandler to process log file changes.
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE_PATH:
            with open(LOG_FILE_PATH, 'r') as file:
                for line in file.readlines():
                    match = LOG_PATTERN.match(line)
                    if match:
                        process_new_log_entry(match)

# Main function to set up file system observer.
def start_log_monitoring():
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(LOG_FILE_PATH), recursive=False)

    try:
        observer.start()
        print('Log monitoring has started. Press Ctrl+C to stop.')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('Log monitoring has stopped.')
    observer.join()

if __name__ == '__main__':
    start_log_monitoring()
