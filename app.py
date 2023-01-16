from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)

from dotenv import load_dotenv

import os, certifi, jwt, hashlib, datetime

load_dotenv() # 환경변수 불러오기

app.config['JSON_AS_ASCII'] = False # UTF-인코딩
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
def dologin():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    all_members = list(db.members.find({'member_id': id_receive},{'_id':False}))
    all_trainers = list(db.trainers.find({'trainer_id': id_receive},{'_id':False}))

    result = {}
    if len(all_members) == 0:
        result = db.trainers.find_one({'id': id_receive, 'pw': pw_hash})
    elif len(all_trainers) == 0:
        result = db.members.find_one({'id': id_receive, 'pw': pw_hash})

    if result != {}:
        return jsonify({'result': 'success'})

    return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.`'})

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


@app.route('/api/reservation')
def reservation_view():
    return render_template('reservation.html', trainer_key=1, member_key=1)

# 회원 예약 신청
@app.route('/api/reservation/member/apply/<int:trainer_key>', methods=['POST'])
def reservation_member_apply(trainer_key):
    # TODO - [~] 멤버키 파라미터 유효성 검사
    member_key = request.form['member_key']
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
    member_key = request.form['member_key']
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
    trainer_key = request.form['trainer_key']
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
    trainer_key = request.form['trainer_key']
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
    trainer_key = request.form['trainer_key']
    exist_member = list(db.members.find({'key': int(member_key)}, {'_id': False}))
    if len(exist_member) == 0:
        return jsonify({'msg': '유효하지 않은 트레이너 키 입니다.'}), 404

    exist_reservation = list(db.reservations.find({'member_key': int(member_key), 'trainer_key': int(trainer_key) }))
    reservation_key = exist_reservation[0]['key']

    db.reservations.delete_one({'key': reservation_key})
    return jsonify({'msg': '멤버 예약이 취소되었습니다.'}), 201

@app.route('/trainer')
def trainer_view():
    trainer_list = list(db.healthin.find({}, {'_id': False}).sort('name', -1))
    return render_template('trainer.html')

@app.route("/api/trainer/check", methods = ["GET"])
def trainer_get():
    trainer_list = list(db.healthin.find({},{'_id':False}))
    return jsonify({'trainer_list': trainer_list})


@app.route("/api/trainer/register", methods = ["POST"])
def trainer_post():
    name_receive= request.form['name_give']
    region_receive= request.form['region_give']
    category_receive= request.form['category_give']
    timetable_receive= request.form['timetable_give']
    price_receive= request.form['price_give']
    description_receive= request.form['description_give']

    doc = {
        'key':0,
        'trainer_id': 'trainer1',
        'password':'abcd1234',
        'name':name_receive,
        'region':region_receive,
        'category' : category_receive,
        'timetable':timetable_receive,
        'price': price_receive,
        'description':description_receive
    }

    db.healthin.insert_one(doc)
    return jsonify({'msg':'등록완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv('PORT'), debug=True)