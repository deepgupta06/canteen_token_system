# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 12:54:23 2021

@author: deep.g
"""
from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect,
    g
)

from create_database import DatabaseOp



# g - object work similarly as global work


class User:
    def __init__(self, id, username, password, group):
        self.id = id
        self.username = username
        self.password = password
        self.group = group

    def __repr__(self):
        return f'<User: {self.username}>'


app = Flask(__name__)
app.secret_key = "janinaja"
users={}
users["login_user_emp"] = ""
users["login_user_fname"] = ""
users["login_user_lname"] = ""
users["login_user_id"] = ""
users["login_user_pw"] = ""
users["login_group"] = ""
user =""
@app.before_request
def before_request():
    global users
    global user
    if "user_id" in session:
        if users["login_user_id"] == session["user_id"]:
            user=users["login_user_emp"]
        g.users = users

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        print(username)

        database = DatabaseOp("canteen_new1.db")
        data_fatching = database.get_userid_pw("empinfo",username)
        for i in data_fatching:
            users["login_user_emp"] = i[0]
            users["login_user_fname"] = i[1]
            users["login_user_lname"] = i[2]
            users["login_user_id"] = i[3]
            users["login_user_pw"] = i[4]
            users["login_group"] = i[5]
            
        
        if users["login_user_id"]==username and users["login_user_pw"] == password:
            session["user_id"] = users["login_user_emp"]
            g.users=users
            return redirect("profile")
        return redirect("login")

    return render_template("login_main.html")


@app.route("/profile")
def profile():
    return render_template("profile_page.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    login_user_emp=""
    login_user_fname=""
    login_user_lname=""
    login_user_id=""
    login_user_pw=""
    login_group=""
    user=""

    return render_template("log_out.html")

@app.route("/recharge")
def recharge():
    if request.method == "POST":
        present_recharge_emp_id = request.form["empid"]
        present_recharge_amount = request.form["amount"]
    return render_template("recharge.html")

@app.route("/availablebalance")
def availablebalance():
    return render_template("available_balance.html")

@app.route("/bookinghistory")
def bookinghistory():
    return render_template("booking_history.html")

@app.route("/recharge_status")
def recharge_status():
    return render_template("recharge_status.html")

@app.route("/adduser", methods=["GET", "POST"])
def adduser():
    if request.method == "POST":
        adding_emp_id = int(request.form["empid"])
        adding_emp_f_name = request.form["firstname"]
        adding_emp_l_name = request.form["lastname"]
        adding_emp_usergroup = request.form["usergroup"]
        adding_emp_userid = adding_emp_f_name+"."+adding_emp_l_name[0]
        adding_emp_pass = adding_emp_userid
        database = DatabaseOp("canteen_new1.db")
        values = [(adding_emp_id,
                   adding_emp_f_name,
                   adding_emp_l_name,
                   adding_emp_userid,
                   adding_emp_pass,
                   adding_emp_usergroup)]
        database.inserting_values("empinfo", values)
        print(values)
        
        return redirect("useraddingstatus")
        
    return render_template("adduser.html")

@app.route("/useraddingstatus")
def useraddingstatus():
    return render_template("useraddingstatus.html")

if __name__ == '__main__':
    app.debug = True
    app.run("192.168.72.186", port=5000)
