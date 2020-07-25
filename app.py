import os
from typing import List
from flask import Flask, render_template, url_for
import firebase_admin
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentSnapshot
from firebase_admin.credentials import Certificate
from firebase_admin import firestore
from firebase_admin.db import Query

PROJECT_ID = 'mywebpage-3a2bd'
SERVICE_ACCOUNT_KEY_PATH = '/Users/Hiroki/Applications/PythonProjects/flask_test/mywebpage-3a2bd-firebase-adminsdk-o3ntg-8a383c01f5.json'
app = Flask(__name__)
cred = Certificate(SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred, dict(projectId=PROJECT_ID))

db: Client = firestore.client()
users_ref = db.collection(u'users')
docs: Query = users_ref.start_at(dict(username='hiroki'))
# print(docs.get())


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


def regist_user(user_name: str, password: str) -> None:
    return


def find_by_user(username: str):
    return


class User(object):
    def __init__(self, user_name: str, email: str):
        """
        """
        super().__init__()
        self.__user_name = user_name
        self.__email = email
        return

    @property
    def user_name(self) -> str:
        return self.__user_name

    @user_name.setter
    def user_name(self, user_name) -> None:
        self.__user_name = user_name
        return

    @property
    def email_address(self) -> str:
        return self.__email

    @email_address.setter
    def email_address(self, email) -> None:
        self.__email = email
        return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
