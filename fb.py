import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import os

def firebase_connection():
    cred = credentials.Certificate(os.getcwd() + '/key.json')
    app = firebase_admin.initialize_app(cred, {
        'projectId': 'proektorium-rsm'
    })
    db = firestore.client(app=app)
    return db, app, cred
    
def parse_results(db, coll='today_details'):
    data = db.collection(coll).stream()
    out = []
    for d in data:
        out.append(d.to_dict())
    return out
