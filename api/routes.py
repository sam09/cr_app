from flask import Flask, jsonify, request
from pymongo import MongoClient
from helper import valid_login, validate_user
from config import db
from timetable import get_timetable
from classes import get_pending_classes, set_pending_classes
from attendance import get_attendance, update_attendance

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
  if request.method == "POST":
     username = request.form['username']
     password = request.form['password']
     return valid_login(username,password)

@app.route('/signup', methods=['POST'])
def signup():
  if request.method == "POST":
     username = request.form['username']
     batch = request.form['batch']
     dept = request.form['department']
     try:
	batch  = int(batch)
     except:
	return jsonify({'Signed Up':0})
     user = {
	      "username" :username,
	      "batch" :batch,
	      "department" :dept,
        "attendance" :[]
	    }
     if validate_user(user):
	print user
	db.users.insert(user)
        return jsonify({"Signed Up" :1})
     return jsonify({"Signed Up" :0})

@app.route('/home/<username>', methods=['GET'])
def getTimeTable(username):
  tt = get_timetable(username) 
  return tt

@app.route('/pending/<username>', methods=['GET'])
def getPending(username):
  if request.method == "GET":
    return get_pending_classes(username)

@app.route('/update/<username>', methods=['POST'])
def setPending(username):
  if request.method == "POST":
    cid = int(request.form['id'])
    p = request.form['presence']
    return set_pending_classes(username, cid, p)

@app.route('/attendance/view/<username>', methods=['POST'])
def getAttendance(username):
  if request.method== "POST":
    sub = request.form['subject']
    return get_attendance(username, sub)

@app.route('/attendance/update/<username>', methods=['POST'])
def updateAttendance(username):
  if request.method == "POST":
    id = int(request.form["id"])
    value = request.form["presence"]
    return update_attendance(username, id, value)

if __name__ =="__main__":
  app.run(debug=True)

