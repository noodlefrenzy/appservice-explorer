from flask import Flask
import os
import socket
import sys
import time
import uuid
from azure.storage.table import TableService, Entity

def init_table():
    table_service = TableService(account_name=os.environ['STORAGE_ACCOUNT_NAME'], account_key=os.environ['STORAGE_ACCOUNT_KEY'])

    table_name = os.environ['TABLE_NAME']
    table_service.create_table(table_name)

    pk = socket.gethostname()
    rkroot = str(uuid.uuid4())

    return { 'service': table_service, 'name': table_name, 'pk': pk, 'rk': rkroot }

def write_entry(table_settings, entry):
    if 'PartitionKey' not in entry:
        entry['PartitionKey'] = table_settings['pk']
    if 'RowKey' not in entry:
        entry['RowKey'] = table_settings['rk'] + str(time.time())
    table_settings['service'].insert_entity(table_settings['name'], entry)

def write_msg(table_settings, msg):
    write_entry(table_settings, { 'details': msg })

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    table_settings = init_table()
    write_msg(table_settings, 'Python version: %s' % sys.version)
    app.run()



