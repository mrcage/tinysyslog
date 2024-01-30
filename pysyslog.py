#!/usr/bin/env python

## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.

# Test
# logger --udp -n 192.168.254.124 -P 514 "test"

LOG_FILE = 'logs/syslog.log'
HOST, PORT = "0.0.0.0", 514

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import logging
import socketserver

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

from tinydb import TinyDB
from datetime import datetime

db = TinyDB('logs/syslog.json')
table = db.table('logs')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = bytes.decode(self.request[0].strip())
        print(f"{timestamp} | {self.client_address[0]} | {data}")
        logging.info(str(data))
        table.insert({'timestamp': timestamp, 'client': self.client_address[0], 'payload': data})


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print(f"Listening on {HOST}:{PORT}")
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        db.close()
        print("Crtl+C Pressed. Shutting down.")
