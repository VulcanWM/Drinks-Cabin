from flask import Flask, render_template, request, redirect
import os
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
from functions import getcookie, getuser, gethashpass, addcookie, allusers, makeaccount, delcookie, makeaccountcd, getusercd, workfunc, tipfunc, dailyfunc

@app.route("/")
def main():
  cookie = str(getcookie("User"))
  user = getuser(cookie)
  ready = getusercd(cookie)
  return render_template("index.html", cookie=cookie, user=user, ready=ready)

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == "POST":
    if getcookie("User") != False:
      return render_template("error.html", error="You have already logged in!")
    username = request.form['namelogin']
    if getuser(username) == False:
      return render_template("error.html", error="That is not the name of a Cabin!")
    password = request.form['passwordl']
    if check_password_hash(gethashpass(username), password) == False:
      return render_template("error.html", error="Wrong password!")
    addcookie("User", username)
    return redirect("/")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
  if request.method == "POST":
    if getcookie("User") != False:
      return render_template("error.html", error="You have already logged in!")
    username = request.form['names']
    if username.lower() in allusers():
      return render_template("error.html", error="A user has this username! Try another one!")
    password = request.form['passwords']
    passworda = request.form['passwordagain']
    if password != passworda:
      return render_template("error.html", error="The two passwords don't match!")
    makeaccount(username, password)
    makeaccountcd(username)
    addcookie("User", username)
    return redirect("/")

@app.route("/logout")
def logout():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  delcookie("User")
  return redirect("/")

@app.route("/work")
def work():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  every = workfunc(getcookie("User"))
  if every == False:
    return render_template("error.html", error="Chill, enjoy your break!")
  return render_template("success.html", type="work", every=every)

@app.route("/tips")
def tips():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  tip = tipfunc(getcookie("User"))
  if tip == False:
    return render_template("error.html", error="Don't shoo away your customers by asking them for tips!")
  return render_template("success.html", type="tip", tip=tip)

@app.route("/daily")
def daily():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  daily = dailyfunc(getcookie("User"))
  if daily == False:
    return render_template("error.html", error="Don't be too greedy!")
  return render_template("success.html", type="daily", daily=daily)