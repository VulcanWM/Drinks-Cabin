from flask import Flask, render_template, request, redirect
import os
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
from functions import getcookie, getuser, gethashpass, addcookie, allusers, makeaccount, delcookie, makeaccountcd, getusercd

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