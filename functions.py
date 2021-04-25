import pymongo
import dns
import datetime
import random
import os
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
clientm = os.getenv("clientm")
mainclient = pymongo.MongoClient(clientm)
usersdb = mainclient.Profiles
profilescol = usersdb.Users
cooldowndb = mainclient.Cooldown
cooldowncol = cooldowndb.Cooldown

def addcookie(key, value):
  session[key] = value

def delcookie(keyname):
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False

def makeaccount(username, password):
  passhash = generate_password_hash(password)
  document = [{
    "Username": username,
    "Password": passhash,
    "Money": "0.00",
    "Drinks": 0,
    "Menu": [{"Type": "Popular", "Name": "Water", "Price": "1.00"}]
  }]
  profilescol.insert_many(document)

def gethashpass(username):
  for user in profilescol.find():
    if user['Username'] == username:
      return user['Password']
  return False

def getuser(username):
  for user in profilescol.find():
    if user['Username'] == username:
      return user
  return False

def allusers():
  users = []
  for user in profilescol.find():
    users.append(user['Username'].lower())
  return users


def makeaccountcd(username):
  document = [{
    "Username": username,
    "Work": None,
    "Tip": None,
    "Overtime": None,
    "Daily": None
  }]
  cooldowncol.insert_many(document)

"""
add time to the work, tip or Overtime
current = dt.datetime.utcnow()
year = str(current).split("-")[0]
month = str(current).split("-")[1]
daypart = str(current).split("-")[2]
day = str(daypart).split()[0]
something1 = str(current).split()[1]
something = something1.split(".")[0]
hour = something.split(":")[0]
minute = something.split(":")[1]
second = something.split(":")[2]
thetime = year + " " + month + " " + day + " " + hour + " " + minute + " " + second
"""

def getusercd(username):
  user = {}
  for uservalue in cooldowncol.find():
    if str(uservalue['Username']) == str(username):
      user['hello'] = True
  if "hello" not in user:
    return False
  cd = []
  things = ["Work", "Tip", "Overtime", "Daily"]
  for uservalue in cooldowncol.find():
    if str(uservalue['Username']) == str(username):
      user = uservalue
      thetime = uservalue['Work']
  if user['Work'] == None:
    cd.append("Ready")
  else:
    a = datetime.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 600:
      cd.append("Ready")
    else:
      cd.append(f"{str(seconds)} left")
  if user['Tip'] == None:
    cd.append("Ready")
  else:
    a = dt.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = dt.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 300:
      cd.append("Ready")
    else:
      cd.append(f"{str(seconds)} left")
  if user['Overtime'] == None:
    cd.append("Ready")
  else:
    a = dt.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = dt.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 1800:
      cd.append("Ready")
    else:
      cd.append(f"{str(seconds)} left")
  if user['Daily'] == None:
    cd.append("Ready")
  else:
    a = dt.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = dt.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 86400:
      cd.append("Ready")
    else:
      cd.append(f"{str(seconds)} left")
  return cd
  
def workfunc(username):
  if getusercd(username)[0] != "Ready":
    return False
  user = getuser(username)
  stuff = []
  total = 0
  amountto = 0
  for item in user['Menu']:
    amount = random.randint(1,100)
    earned = float(item['Price']) * amount
    theitem = {"Amount": str(amount), "Item": item["Name"], "Earned": str(earned)}
    stuff.append(theitem)
    amountto = amountto + amount
    total = total + float(earned)
  every = {"Stuff": stuff, "Total": total}
  for uservalue in profilescol.find():
    if uservalue['Username'] == username:
      user2 = uservalue
      newto = float(user2['Drinks']) + float(amountto)
      del user2['Drinks']
      user2['Drinks'] = amountto
      newam = str(float(user2['Money']) + float(total))
      newam = str(newam) + "0"
      del user2['Money']
      user2['Money'] = newam
      delete = {"_id": uservalue['_id']}
      profilescol.delete_one(delete)
      profilescol.insert_many([user2])
  for uservalue in cooldowncol.find():
    if uservalue['Username'] == username:
      current = datetime.datetime.utcnow()
      year = str(current).split("-")[0]
      month = str(current).split("-")[1]
      daypart = str(current).split("-")[2]
      day = str(daypart).split()[0]
      something1 = str(current).split()[1]
      something = something1.split(".")[0]
      hour = something.split(":")[0]
      minute = something.split(":")[1]
      second = something.split(":")[2]
      thetime = year + " " + month + " " + day + " " + hour + " " + minute + " " + second
      user2 = uservalue
      del user2['Work']
      user2['Work'] = thetime
      delete = {"_id": uservalue['_id']}
      cooldowncol.delete_one(delete)
      cooldowncol.insert_many([user2])
  return every