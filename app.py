import firebase_admin
from firebase_admin import credentials, auth
import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/test", methods=['POST'])
def test():
    return 'TEST SUCCESS'


@app.route("/naver-oauth", methods=['POST'])
def get_naver_oauth():
    if (request.data):
        naver_login_url = 'https://openapi.naver.com/v1/nid/me'
        headers = {'Authorization': f'Bearer {request.json["token"]}'}
        result = requests.get(naver_login_url, headers=headers)
        return result.json()
    return 'Need Access Token'


@app.route('/custom-token', methods=['POST'])
def create_custom_token():
    if (request.data):
        uid = request.json["uid"]
        custom_token = auth.create_custom_token(uid)
        return custom_token
    return 'Need UID'


@app.route('/upload', methods=['POST'])
def upload_students():
    return request.form.get('file')


app.run(debug=True, host="0.0.0.0", port=8090)
