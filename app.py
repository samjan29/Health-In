from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
import os
from pymongo import MongoClient, ReturnDocument

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # UTF-인코딩
load_dotenv() # 환경변수 불러오기

# DB 환경설정
client = MongoClient(os.getenv('DB_URL'))
db = client.hanghae_mini

@app.route('/')
def home():
    return render_template('index.html')

# 회원 예약 신청
@app.route('/api/reservation/member/apply/<int:trainer_key>')
def reservation_member_apply(trainer_key):
    # TODO - [] 파라미터 받기
    # TODO - [] 멤버 식별하고 멤버 키 가져오기
    # TODO - [] 예약 doc 생성
    # TODO - [] 결과
    return 'reservation member apply'

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
