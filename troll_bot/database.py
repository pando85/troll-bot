import os

from pymongo import MongoClient
from flask import g

from troll_bot import app

HOST = os.environ['DB_HOST']
PORT = int(os.environ['DB_PORT']) 

@app.before_request
def connect_db():
    g.db_client = MongoClient(HOST, PORT)


@app.after_request
def close_connection(response):
    g.db_client.close()
    return response