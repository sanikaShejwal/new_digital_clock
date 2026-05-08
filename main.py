from flask import Flask, request, send_from_directory
import firebase_admin
from firebase_admin import credentials, auth
from google.cloud import datastore

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKeys.json")
firebase_admin.initialize_app(cred)

datastore_client = datastore.Client.from_service_account_json("serviceAccountKeys.json")

# 👇 Serve index.html
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization').split("Bearer ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token['email']

        key = datastore_client.key('User', uid)
        entity = datastore.Entity(key)
        entity.update({
            "email": email
        })

        datastore_client.put(entity)

        return "User Verified & Stored", 200

    except Exception as e:
        return str(e), 401

if __name__ == '__main__':
    app.run(debug=True)