# import pymongo
# import os
# clientm = os.getenv("clientm")
# mainclient = pymongo.MongoClient(clientm)
# smdb = mainclient.SM
# smcol = smdb.SM
# def strawmarket():
#   document = [{
#     "Color": "Red",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Orange",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Yellow",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Green",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Blue",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Indigo",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   },
#   {
#     "Color": "Violet",
#     "Price": 100,
#     "Change": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   }]
#   smcol.insert_many(document)
#   return True