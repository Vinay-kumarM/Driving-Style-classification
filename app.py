import numpy as np
from flask import Flask,request,jsonify,render_template
import joblib
import sqlite3
import pandas as pd
#import cv2

import joblib
filename = 'model.sav'
model = joblib.load(filename)

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")


@app.route('/index')
def index():
	return render_template('index.html')



@app.route('/predict',methods=['POST'])
def predict():

    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]

    predict = model.predict(final4)
    if predict == 0:
        output = 'Driving Style is AGGRESSIVE!'
    elif predict == 1:
        output = 'Driving Style is CONSERVATIVE!'
    elif predict == 2:
        output = 'Driving Style is NORMAL!'
 
    return render_template('result.html',output=output)





@app.route('/notebook')
def notebook1():
	return render_template('DrivingStylePrediction.html')



@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
    app.run()
