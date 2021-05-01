import pymongo
import dns
import datetime
import random
import os
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from lists import decorations, upgrades, employees
clientm = os.getenv("clientm")
mainclient = pymongo.MongoClient(clientm)
usersdb = mainclient.Profiles
profilescol = usersdb.Users
cooldowndb = mainclient.Cooldown
cooldowncol = cooldowndb.Cooldown
hourlydb = mainclient.Hourly
hourlycol = hourlydb.Hourly

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
    "Hourly": 0,
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
    thetime = user['Work']
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
      cd.append(f"{str(600 - seconds)} seconds left")
  if user['Tip'] == None:
    cd.append("Ready")
  else:
    thetime = user['Tip']
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
    if seconds > 300:
      cd.append("Ready")
    else:
      cd.append(f"{str(300 - seconds)} seconds left")
  if user['Overtime'] == None:
    cd.append("Ready")
  else:
    thetime = user['Overtime']
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
    if seconds > 1800:
      cd.append("Ready")
    else:
      cd.append(f"{str(1800 - seconds)} seconds left")
  if user['Daily'] == None:
    cd.append("Ready")
  else:
    thetime = user['Daily']
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
    if seconds > 86400:
      cd.append("Ready")
    else:
      cd.append(f"{str(84000 - seconds)} seconds left")
  return cd
  
def workfunc(username):
  if getusercd(username)[0] != "Ready":
    return False
  user = getuser(username)
  stuff = []
  total = 0
  amountto = user['Drinks']
  for item in user['Menu']:
    amount = random.randint(1,100)
    earned = float(item['Price']) * amount
    for item in user['Menu']:
      if item['Name'] == "Water":
        emoji = "🥤"
      elif item['Type'] == "Popular":
        emoji = "🫖"
      elif item['Type'] == "Juice":
        emoji = "🍹"
      elif item['Type'] == "Alcoholic":
        emoji = "🍺"
    theitem = {"Amount": str(amount), "Item": item["Name"], "Earned": str(earned) + "0", "Emoji": emoji}
    stuff.append(theitem)
    amountto = amountto + amount
    total = total + float(earned)
  total = str(total) + "0"
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

def dailyfunc(username):
  if getusercd(username)[3] != "Ready":
    return False
  user = getuser(username)
  for uservalue in profilescol.find():
    if uservalue['Username'] == username:
      user2 = uservalue
      newam = str(float(user2['Money']) + float(500.0))
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
      del user2['Daily']
      user2['Daily'] = thetime
      delete = {"_id": uservalue['_id']}
      cooldowncol.delete_one(delete)
      cooldowncol.insert_many([user2])
  return "You have claimed your ₹25000.00 daily reward!"

def tipfunc(username):
  if getusercd(username)[1] != "Ready":
    return False
  user = getuser(username)
  tips = random.randint(1,500)
  for uservalue in profilescol.find():
    if uservalue['Username'] == username:
      user2 = uservalue
      newam = str(float(user2['Money']) + float(tips))
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
      del user2['Tip']
      user2['Tip'] = thetime
      delete = {"_id": uservalue['_id']}
      cooldowncol.delete_one(delete)
      cooldowncol.insert_many([user2])
  return tips

def checkhourly():
  for hourly in hourlycol.find():
    if hourly['_id'] == 1:
      return hourly['Hourly']
    
def makeaccounthr(username):
  document = [{
    "Username": username,
    "Boosts": {},
    "Employees": {},
    "Upgrades": {},
    "Decorations": {}
  }]
  hourlycol.insert_many(document)

def getpriceempl(username, name):
  if name not in employees:
    return False
  for user in hourlycol.find():
    if user['_id'] != 1:
      if user['Username'] == username:
        if name in user['Employees']:
          amount = user['Employees'][name]
          if int(amount) == 10:
            return "Hit max amount"
        else:
          amount = 0
        hourly = employees[name]
        price = (1 + amount) * (25 * float(hourly))
        return price

def getpricedeco(username, name):
  if name not in decorations:
    return False
  for user in hourlycol.find():
    if user['_id'] != 1:
      if user['Username'] == username:
        if name in user['Decorations']:
          amount = user['Decorations'][name]
          if int(amount) == 10:
            return "Hit max amount"
        else:
          amount = 0
        hourly = decorations[name]
        price = (1 + amount) * (25 * float(hourly))
        return price

def getpriceup(username, name):
  if name not in upgrades:
    return False
  for user in hourlycol.find():
    if user['_id'] != 1:
      if user['Username'] == username:
        if name in user['Upgrades']:
          amount = user['Upgrades'][name]
          if int(amount) == 10:
            return "Hit max amount"
        else:
          amount = 0
        hourly = upgrades[name]
        price = (1 + amount) * (25 * float(hourly))
        return price

def buydeco(username, item):
  price = getpricedeco(username, item)
  if price == False:
    return "This item doesn't exist"
  if price == "Hit max amount":
    return f"You cannot have more than 10 of {item}"
  if float(getuser(username)['Money']) < float(price):
    return "You don't have enough money to buy this item!"
  for user in hourlycol.find():
    if user['_id'] != 1 and user['Username'] == username:
      user2 = user
      if item in user['Decorations']:
        decodict = user['Decorations']
        number = user2['Decorations'][item]
        del user2['Decorations'][item]
        user2['Decorations'][item] = number + 1
      else:
        user2['Decorations'][item] = 1
      delete = {"_id": user['_id']}
      hourlycol.delete_one(delete)
      hourlycol.insert_many([user2])
  for user in profilescol.find():
    if user['Username'] == username:
      user2 = user
      money = user2['Money']
      del user2['Money']
      hourly = user2['Hourly']
      del user2['Hourly']
      user2['Hourly'] = hourly + int(decorations[item].split(".")[0])
      user2['Money'] = str(float(money) - float(price)) + "0"
      delete = {"_id": user['_id']}
      profilescol.delete_one(delete)
      profilescol.insert_many([user2])
  return True

def buyup(username, item):
  price = getpriceup(username, item)
  if price == False:
    return "This item doesn't exist"
  if price == "Hit max amount":
    return f"You cannot have more than 10 of {item}"
  if float(getuser(username)['Money']) < float(price):
    return "You don't have enough money to buy this item!"
  for user in hourlycol.find():
    if user['_id'] != 1 and user['Username'] == username:
      user2 = user
      if item in user['Upgrades']:
        decodict = user['Upgrades']
        number = user2['Upgrades'][item]
        del user2['Upgrades'][item]
        user2['Upgradess'][item] = number + 1
      else:
        user2['Upgrades'][item] = 1
      delete = {"_id": user['_id']}
      hourlycol.delete_one(delete)
      hourlycol.insert_many([user2])
  for user in profilescol.find():
    if user['Username'] == username:
      user2 = user
      money = user2['Money']
      del user2['Money']
      hourly = user2['Hourly']
      del user2['Hourly']
      user2['Hourly'] = hourly + int(upgrades[item].split(".")[0])
      user2['Money'] = str(float(money) - float(price)) + "0"
      delete = {"_id": user['_id']}
      profilescol.delete_one(delete)
      profilescol.insert_many([user2])
  return True

def buyempl(username, item):
  price = getpriceempl(username, item)
  if price == False:
    return "This employee type doesn't exist"
  if price == "Hit max amount":
    return f"You cannot have more than 10 of {item}"
  if float(getuser(username)['Money']) < float(price):
    return "You don't have enough money to hire this employee type"
  for user in hourlycol.find():
    if user['_id'] != 1 and user['Username'] == username:
      user2 = user
      if item in user['Employees']:
        decodict = user['Employees']
        number = user2['Employees'][item]
        del user2['Employees'][item]
        user2['Employees'][item] = number + 1
      else:
        user2['Employees'][item] = 1
      delete = {"_id": user['_id']}
      hourlycol.delete_one(delete)
      hourlycol.insert_many([user2])
  for user in profilescol.find():
    if user['Username'] == username:
      user2 = user
      money = user2['Money']
      del user2['Money']
      hourly = user2['Hourly']
      del user2['Hourly']
      user2['Hourly'] = hourly + int(employees[item].split(".")[0])
      user2['Money'] = str(float(money) - float(price)) + "0"
      delete = {"_id": user['_id']}
      profilescol.delete_one(delete)
      profilescol.insert_many([user2])
  return True