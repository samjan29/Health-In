from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)

from dotenv import load_dotenv

from datetime import datetime

import os, certifi, jwt, hashlib

load_dotenv() # 환경변수 불러오기
ca=certifi.where()

from pymongo import MongoClient
client = MongoClient(os.getenv('DB_URL'), tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')\

@app.route('/login')
def login():
    return render_template('login.html')

# 회원 가입
@app.route('/api/join', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    role_receive = int(request.form['role_give'])

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'member_id': id_receive,
        'password': pw_hash,
        'nickname': nickname_receive,
        'role': role_receive
    }

    key = 1
    if role_receive == 0:
        all_members = list(db.members.find({}, {'_id': False}))
        if len(all_members) != 0:
            key = all_members[-1]['key'] + 1

        doc['key'] = key
        db.members.insert_one(doc)

    elif role_receive == 1:
        all_trainers = list(db.trainers.find({}, {'_id': False}))
        if len(all_trainers) != 0:
            key = all_trainers[-1]['key'] + 1

        doc['key'] = key
        db.trainers.insert_one(doc)

    return jsonify({'msg': '회원 가입 완료'})

# 외원가입
@app.route('/api/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    return jsonify({'msg': '회원 가입 완료'})

# 리뷰 목록 불러오기
@app.route('/api/trainer/review/<int:key>', methods=['GET'])
def get_reviews(key):
    all_review_key = db.trainer.find_one({'key': int(key)}, {'_id':False})['review_key']

    review_list = []

    for review_key in all_review_key:
        review = db.review.find_one({'key': review_key}, {'_id':False})
        review_list.append(review)

        member = db.member .find_one({'key': review['member_key']}, {'_id':False})
        review_list[-1]['member_name'] = member['nickname']

    return jsonify({'reviewList': review_list})

# 리뷰 저장
@app.route('/api/trainer/review/<int:key>', methods=['POST'])
def set_review(key):
    member_key_receive = int(request.form['member_key_give'])
    rank_receive = int(request.form['rank_give'])
    content_receive = request.form['content_give']

    db.trainer.update_one({'key': key}, {'$push': {'member_key': member_key_receive}})

    review_key = 1
    review_list = list(db.review.find({}, {'_id': False}))

    if len(review_list) != 0:
        review_key = review_list[-1]['key'] + 1

    doc = {
        'key': review_key,
        'member_key': member_key_receive,
        'rank': rank_receive,
        'content': content_receive,
        'created_at': datetime.now().replace(microsecond=0)
    }

    db.review.insert_one(doc)

    return jsonify({'msg': '리뷰 작성 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv('PORT'), debug=True)