from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.s6i4xlw.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

# @app.route("/api/trainer/check", methods = ["GET"])
# def trainer_get():
#     trainer_list = list(db.health_in.find({}))
#     return jsonify({'trainer_list': trainer_list})

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


    return jsonify({'msg':'등록완료!'})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)