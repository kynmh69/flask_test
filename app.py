import os
from flask import Flask, render_template, url_for
import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import firestore

PROJECT_ID = 'mywebpage-3a2bd'
SERVICE_ACCOUNT_KEY_PATH = '/Users/Hiroki/Applications/PythonProjects/flask_test/mywebpage-3a2bd-firebase-adminsdk-o3ntg-8a383c01f5.json'
app = Flask(__name__)
cred = Certificate(SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred, dict(projectId=PROJECT_ID))

db = firestore.client()
users_ref = db.collection(u'users')
docs = users_ref.steam()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))


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
def hello():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
