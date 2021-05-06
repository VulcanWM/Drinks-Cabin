from flask import Flask, render_template, request, redirect
import os
import requests
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
from functions import getcookie, getuser, gethashpass, addcookie, allusers, makeaccount, delcookie, makeaccountcd, getusercd, workfunc, tipfunc, dailyfunc, checkhourly, makeaccounthr, getpriceempl, getpricedeco, getpriceup, buyempl, buydeco, buyup, getamountempl, getamountdeco, getamountup, buymenuitem, getuserfranstats, getuserfranhourly, makefranchise, rolldice, flipcoin, cupgame, getsm, getusersm, buysm, sellsm

from lists import decorations, employees, upgrades

@app.route("/")
def main():
  cookie = str(getcookie("User"))
  if cookie == False:
    return render_template("index.html", cookie=cookie)
  user = getuser(cookie)
  ready = getusercd(cookie)
  useremployees = []
  for employee in employees:
    useremployees.append({"Name": employee, "Boost": f"₹{employees[employee]}/hr", "Price": f"₹{str(getpriceempl(cookie, employee))}0", "Amount": getamountempl(getcookie("User"), employee)})
  userdecos = []
  for deco in decorations:
    userdecos.append({"Name": deco, "Boost": f"₹{decorations[deco]}/hr", "Price": f"₹{str(getpricedeco(cookie, deco))}0", "Amount": getamountdeco(getcookie("User"), deco)})
  userupgrades = []
  for up in upgrades:
    userupgrades.append({"Name": up, "Boost": f"₹{upgrades[up]}/hr", "Price": f"₹{str(getpriceup(cookie, up))}0", "Amount": getamountup(getcookie("User"), up)})
  return render_template("index.html", cookie=cookie, user=user, ready=ready, employees=useremployees, decorations=userdecos, upgrades=userupgrades, franstats=getuserfranstats(cookie), franhourly=getuserfranhourly(cookie), sms=getusersm(cookie))

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
    makeaccounthr(username)
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
  if checkhourly() == True:
    return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
  every = workfunc(getcookie("User"))
  if every == False:
    return render_template("error.html", error="Chill, enjoy your break!")
  return render_template("success.html", type="work", every=every)

@app.route("/tips")
def tips():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  if checkhourly() == True:
    return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
  tip = tipfunc(getcookie("User"))
  if tip == False:
    return render_template("error.html", error="Don't shoo away your customers by asking them for tips!")
  return render_template("success.html", type="tip", tip=tip)

@app.route("/daily")
def daily():
  if getcookie("User") == False:
    return render_template("error.html", error="You have not logged in!")
  if checkhourly() == True:
    return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
  daily = dailyfunc(getcookie("User"))
  if daily == False:
    return render_template("error.html", error="Don't be too greedy!")
  return render_template("success.html", type="daily", daily=daily)

@app.route("/shop", methods=['POST', 'GET'])
def shop():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    if request.form['category'] == "decorations":
      func = buydeco(getcookie("User"), request.form['title'])
      if func == True:
        return render_template("success.html", item=request.form['title'], type='buy')
      else:
        return render_template("error.html", error=func)
    if request.form['category'] == "upgrades":
      func = buyup(getcookie("User"), request.form['title'])
      if func == True:
        return render_template("success.html", item=request.form['title'], type='buy')
      else:
        return render_template("error.html", error=func)
    if request.form['category'] == "employees":
      func = buyempl(getcookie("User"), request.form['title'])
      if func == True:
        return render_template("success.html", item=request.form['title'], type='hire')
      else:
        return render_template("error.html", error=func)

@app.route("/buymenuslot", methods=['POST', 'GET'])
def buymenuslot():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    item = request.form['title']
    func = buymenuitem(getcookie("User"), item)
    if func == True:
      return render_template("success.html", type="buymenu", item=item)
    return render_template("error.html", error=func)

# @app.route("/makefranchise", methods=['POST', 'GET'])
# def makefranchiseapp():
#   if request.method == "POST":
#     if getcookie("User") == False:
#       return render_template("error.html", error="You have not logged in!")
#     if checkhourly() == True:
#       return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
#     name = request.form['name']
#     tag = request.form['tag']
#     func = makefranchise(getcookie("User"), tag, name)
#     if func == True:
#       return render_template("success.html", type="makefranchise", name=name, tag=tag)
#     return render_template("error.html", error=func)

@app.route("/rolldice", methods=['POST', 'GET'])
def rollapp():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    number = request.form['number']
    bet = request.form['bet']
    func = rolldice(getcookie("User"), number, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", type="gambling", success=func)

@app.route("/flipcoin", methods=['POST', 'GET'])
def flipapp():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    side = request.form['side']
    bet = request.form['bet']
    func = flipcoin(getcookie("User"), side, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", type="gambling", success=func)

@app.route("/cupgame", methods=['POST', 'GET'])
def cupapp():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    number = request.form['number']
    bet = request.form['bet']
    func = cupgame(getcookie("User"), number, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", type="gambling", success=func)

@app.route("/sm/<color>")
def sm(color):
  if getsm(color) == False:
    return "This color doesn't exist in the straw market!"
  response = requests.get(f"https://Drinks-Cabin-SM-Graph.vulcanwm.repl.co/color/{color}")
  url = str(response.content)
  url = url.replace("b'", "")
  url = url[:-1]
  price = getsm(color)['Price']
  return f'<img src="{url}" alt="Graph" width="1000" length="300"><br><p>Price per straw: ₹{price}</p><br><br><a href="/">Home</a>'

@app.route("/buystraw", methods=['POST', 'GET'])
def buystraw():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    number = request.form['amount']
    color = request.form['color']
    if int(number) > 5000:
      return "You cannot buy more than 5000 of each straw!"
    func = buysm(color, getcookie("User"), number)
    if func == True:
      return render_template("success.html", type="buystraw")
    else:
      return render_template("error.html", error=func)

@app.route("/sellstraw", methods=['POST', 'GET'])
def sellstraw():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("error.html", error="You have not logged in!")
    if checkhourly() == True:
      return render_template("error.html", error="Hourly incomes are being sent out. Try again in a few seconds!")
    amount = request.form['amount']
    color = request.form['color']
    func = sellsm(getcookie("User"), color, amount)
    if type(func) is dict:
      return render_template("success.html", dict=func, type="sellstraw")
    else:
      return render_template("error.html", error=func)
  
@app.route("/rules")
def rules():
  return render_template("rules.html")