from flask import Flask, render_template, request

app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('여기에 URL 입력')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')