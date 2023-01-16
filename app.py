from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from dotenv import load_dotenv

from datetime import datetime

import os

load_dotenv() # 환경변수 불러오기
app.config['JSON_AS_ASCII'] = False # UTF-인코딩

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


@app.route('/api/reservation')
def reservation_view():
    return render_template('reservation.html', trainer_key=1)

# 회원 예약 신청
@app.route('/api/reservation/member/apply/<int:trainer_key>', methods=['POST'])
def reservation_member_apply(trainer_key):
    # TODO - [~] 멤버키 파라미터 유효성 검사
    member_key = request.headers['member_key']
    ## TODO - [] member_key가 없는 경우 추가
    if member_key is None:
        return jsonify({'msg': '멤버 키를 입력해주세요'}), 400

    # TODO - [x] 트레이너키 파라미터 유효성 검사
    exist_trainer = list(db.trainers.find({'key': int(trainer_key)}, {'_id': False}))
    if len(exist_trainer) == 0:
        return jsonify({'msg': '유효하지 않은 트레이너 키 입니다.'}), 404

    # TODO - [x] 예약 키 생성
    reservation_key = 1
    reservation_list = list(db.reservations.find({}, {'_id': False }))
    if len(reservation_list) != 0:
        reservation_key = reservation_list[-1]['key'] + 1
    # TODO - [x] 예약 doc 생성
    doc = {
        'key': int(reservation_key),
        'member_key': int(member_key),
        'trainer_key': int(trainer_key),
        'reserve_status': 0,
        'reserve_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    }
    db.reservations.insert_one(doc)
    # TODO - [x] 결과
    return jsonify({'msg': '트레이너 예약 신청이 완료되었습니다.'}), 201

# 회원 예약 취소
@app.route('/api/reservation/member/cancel/<int:trainer_key>', methods=['DELETE'])
def reservation_member_cancel(trainer_key):
    # TODO - [] 파라미터 유효성 검사
    member_key = request.headers['member_key']
    exist_trainer = list(db.trainers.find({'key': int(trainer_key)}, {'_id': False}))
    if len(exist_trainer) == 0:
        return jsonify({'msg': '유효하지 않은 트레이너 키 입니다.'}), 404

    exist_reservation = list(db.reservations.find({'member_key': int(member_key), 'trainer_key': trainer_key }, {'_id': False}))
    reservation_key = exist_reservation[0]['key']

    db.reservations.delete_one({'key': reservation_key})
    return jsonify({'msg': '트레이너 예약 신청이 취소되었습니다.'}), 201

# 트레이너 예약 승인
@app.route('/api/reservation/trainer/confirm/<int:member_key>', methods=['POST'])
def reservation_trainer_confirm(member_key):
    # TODO - [] 파라미터 유효성 검사
    trainer_key = request.headers['trainer_key']
    exist_member = list(db.members.find({'key': int(member_key)}, {'_id': False}))
    if len(exist_member) == 0:
        return jsonify({'msg': '유효하지 않은 멤버 키 입니다.'}), 404

    exist_reservation = list(
        db.reservations.find({'member_key': int(member_key), 'trainer_key': int(trainer_key)})
    )
    reservation_key = exist_reservation[0]['key']

    db.reservations.update_one({'key': reservation_key}, {'$set': { 'reserve_status': 1 }})
    return jsonify({'msg': '멤버 예약 승인이 완료되었습니다.'}), 201

# 트레이너 예약 진행 완료
@app.route('/api/reservation/trainer/complete/<int:member_key>', methods=['POST'])
def reservation_trainer_complete(member_key):
    # TODO - [] 파라미터 유효성 검사
    trainer_key = request.headers['trainer_key']
    exist_member = list(db.members.find({'key': int(member_key)}, {'_id': False}))
    if len(exist_member) == 0:
        return jsonify({'msg': '유효하지 않은 멤버 키 입니다.'}), 404

    exist_reservation = list(
        db.reservations.find({'member_key': int(member_key), 'trainer_key': int(trainer_key)})
    )
    reservation_key = exist_reservation[0]['key']

    db.reservations.update_one({'key': reservation_key}, {'$set': { 'reserve_status': 2 }})

    return jsonify({'msg': '멤버 예약 진행이 완료되었습니다.'}), 201

# 트레이너 예약 취소
@app.route('/api/reservation/trainer/cancel/<int:member_key>', methods=['DELETE'])
def reservation_trainer_cancel(member_key):
    # TODO - [] 파라미터 유효성 검사
    trainer_key = request.headers['trainer_key']
    exist_member = list(db.members.find({'key': int(member_key)}, {'_id': False}))
    if len(exist_member) == 0:
        return jsonify({'msg': '유효하지 않은 트레이너 키 입니다.'}), 404

    exist_reservation = list(db.reservations.find({'member_key': int(member_key), 'trainer_key': int(trainer_key) }))
    reservation_key = exist_reservation[0]['key']

    db.reservations.delete_one({'key': reservation_key})
    return jsonify({'msg': '멤버 예약이 취소되었습니다.'}), 201


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv('PORT'), debug=True)
