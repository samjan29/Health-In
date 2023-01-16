from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
import os
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # UTF-인코딩
load_dotenv() # 환경변수 불러오기

# DB 환경설정
client = MongoClient(os.getenv('DB_URL'))
db = client.hanghae_mini

@app.route('/api/reservation')
def home():
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
    exist_trainer_key = list(db.trainers.find({'key': int(trainer_key)}, {'_id': False}))
    if len(exist_trainer_key) == 0:
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
    return jsonify({'msg': 'success'}), 201

# 회원 예약 취소
@app.route('/api/reservation/member/cancel/<int:trainer_key>')
def reservation_member_cancel(trainer_key):
    # TODO - [] 파라미터 받기
    # TODO - [] 멤버 식별하고 멤버 키 가져오기
    # TODO - [] 예약 상태 변경
    # TODO - [] 결과
    return 'reservation member cancel'

# 트레이너 예약 승인
@app.route('/api/reservation/trainer/confirm/<int:member_key>')
def reservation_trainer_confirm(member_key):
    # TODO - [] 파라미터 받기
    # TODO - [] 트레이너 식별하고 트레이너 키 가져오기
    # TODO - [] 예약 상태 변경
    # TODO - [] 결과
    return 'reservation trainer cancel'

# 트레이너 예약 진행 완료
@app.route('/api/reservation/trainer/complete/<int:member_key>')
def reservation_trainer_complete(member_key):
    # TODO - [] 파라미터 받기
    # TODO - [] 트레이너 식별하고 트레이너 키 가져오기
    # TODO - [] 예약 상태 변경
    # TODO - [] 결과
    return 'reservation trainer complete'

# 트레이너 예약 취소
@app.route('/api/reservation/trainer/cancel/<int:member_key>')
def reservation_trainer_cancel(member_key):
    # TODO - [] 파라미터 받기
    # TODO - [] 트레이너 식별하고 트레이너 키 가져오기
    # TODO - [] 예약 상태 변경
    # TODO - [] 결과
    return 'reservation trainer cancel'


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
