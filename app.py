from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from dotenv import load_dotenv

from datetime import datetime

import os

load_dotenv() # 환경변수 불러오기

from pymongo import MongoClient
client = MongoClient(os.getenv('DB_URL'))
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

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
    member_key = int(request.form['member_key'])
    rank = int(request.form['rank'])
    content = request.form['content']

    db.trainer.update_one({'key': key}, {'$push': {'member_key': member_key}})

    review_key = 1
    review_list = list(db.review.find({}, {'_id': False}))

    if len(review_list) != 0:
        review_key = review_list[-1]['key'] + 1

    doc = {
        'key': review_key,
        'member_key': member_key,
        'rank': rank,
        'content': content,
        'created_at': datetime.now().replace(microsecond=0)
    }

    db.review.insert_one(doc)

    return jsonify({'msg': '리뷰 작성 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv('PORT'), debug=True)