import watchdog.events
import watchdog.observers
import time
import constants
from paramiko import Transport, SFTPClient
import errno
import logging
import os
from connect_remote import SftpClient

logging.basicConfig(format='%(levelname)s : %(message)s',level=logging.INFO)

class Handler(watchdog.events.PatternMatchingEventHandler):
	def __init__(self):
		# Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.txt'],
															ignore_directories=True, case_sensitive=False)

	def on_created(self, event):
		print("Watchdog received created event - % s." % event.src_path)
		upload_local_path = event.src_path
		filename = os.path.basename(event.src_path)
		client.file_exists(upload_remote_path)
		client.upload(upload_local_path,upload_remote_path + filename)

	def on_modified(self, event):
		print("Watchdog received modified event - % s." % event.src_path)
		# Event is modified, you can process it now


if __name__ == "__main__":
    host = constants.HOST
    port = constants.PORT
    username = constants.USER
    src_path = r"B:\uploads" # Place your source file directory, for Windows r"B:\uploads", for unix '/home/newfiles/FS/'
    password = constants.PASSWORD
    upload_remote_path = '/home/testing/FS/'	# Place your remote file directory
    client = SftpClient(host, port, username, password)

    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
	       while True:
			            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
