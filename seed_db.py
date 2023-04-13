import os

import model
import requests
from server import app

def create_db():
    os.system(f'dropdb {os.environ["POSTGRES_DB"]}')
    os.system(f'createdb {os.environ["POSTGRES_DB"]}')

def create_users():
    user_data = requests.get('https://jsonplaceholder.typicode.com/users').json()
    for entry in user_data:
        user = model.User(email=entry['email'])
        model.db.session.add(user)
    model.db.session.commit()

with app.app_context():
    create_db()
    model.connect_to_db(app)
    create_users()





