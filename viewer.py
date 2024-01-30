from tinydb import TinyDB
from tabulate import tabulate
import time

db = TinyDB('logs/syslog.json')
table = db.table('logs')

limit = 10

# entries = table.all()
entries = sorted(table.all(), key=lambda x: x.get('timestamp', ''), reverse=True)[:10]


# Print the formatted table
headers = entries[0].keys() if entries else []
rows = [entry.values() for entry in entries]

print(tabulate(rows, headers=headers, tablefmt='pretty', stralign='left'))
