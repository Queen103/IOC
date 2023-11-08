#add thư viện flask
from flask import Flask, jsonify
import pymysql as db
import json as js
import Recognize
import credentials as cr
import requests
import sound as sd

app = Flask(__name__)

should_stop = False

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'Hello World'
	

@app.route('/open')
def get():
	try:
		sd.playsound(cr.movecame)
		id,pic,date = Recognize.recognizerUser()
		print(id,pic,date)
		connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
		curs=connection.cursor()
		sql = "select * from `securitysystem`.`user` where `id` = %s"
		sql1 = "INSERT INTO `securitysystem`.`history` (`userid`, `picid`, `date`) VALUES (%s, %s, %s);"
		url = f"http://{cr.url}/api"
		curs.execute(sql,id)
		data = curs.fetchone()
		if data:
			value = (data[1],pic,date)
			print(value)
			curs.execute(sql1,value)
			sd.playsound(cr.back)
			data = {"data":"1"}
		else:
			data = {"data":"0"}
		print(data)
		response = requests.post(url, data=data)
		print(response.text)
	except:
		print("Lỗi rồi bạn")
	finally:
		connection.commit()
		connection.close()

@app.route('/close')
def close():
	data = {"data":"0"}
	url = f"http://{cr.url}/api"
	print(data)
	response = requests.post(url, data=data)
	print(response.text)

@app.route('/test',methods=['GET'])
def post():
	Recognize.close()
	print("ok duoc roi")

@app.route('/stop_loop', methods=['GET'])
def stop_loop():
    global should_stop
    should_stop = True
    return jsonify({"message": "Dừng vòng lặp thành công"})

@app.route('/check_loop', methods=['GET'])
def check_loop():
    return jsonify({"should_stop": should_stop})

@app.route('/start_loop', methods=['GET'])
def start_loop():
    global should_stop
    should_stop = False
    return jsonify({"message": "Start vòng lặp thành công"})

#chay chương trình run app 
if __name__ == '__main__':
	# run() method of Flask class runs the application 
	# on the local development server.
	app.run(host='0.0.0.0', port=5000)
