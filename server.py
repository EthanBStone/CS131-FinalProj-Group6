
from flask import Flask, redirect, url_for, request
import random
app = Flask(__name__)

random_labels = ['oxygen_mask', 'jersey', 'sweatshirt', 'water_bottle', 'pill_bottle', 'teddy', 'harmonica']
last_label = ""
label_to_find = "water_bottle"
active_ = False #True
labelUpdate = True #False

class Player:
    def __init__(self):
        name = ""
        score = 0

player1Here = False
player2Here = False
player1Score = 0
player2Score = 0
max_score = 4
player1prev = ""
player2prev = ""
player1Updated = False #True
player2Updated = False #True
players = []


# Displays on the web page, not necessary
@app.route("/")
def hello_world():
    return "<h1>This web server is supposed to be functional only</h1>"



@app.route("/data")
def data():
   data = 'fail'
   if 'data' in request.args: 
      data = request.args.get('data')
   return data


@app.route("/playerInput")
def playerInput():
   #global imports
   global random_labels
   global label_to_find
   global active_
   global labelUpdate
   global player1Here
   global player2Here
   global player1Score
   global player2Score
   global max_score
   global player1prev
   global player2prev
   global player1Updated
   global player2Updated
   # globals imports

   data = 'fail'
   if 'data' in request.args: 
      data = request.args.get('data')

   tag = data[0]
   str = data
   str = str[1:]

   #print("input: " + str + "\nlabeltoFind: " + label_to_find)

   if (str == "here"):
      if (tag == '1'):
         player1Here = not player1Here
      elif(tag == '2'):
         player2Here = not player2Here
   
   if ( labelUpdate == True): return "Update not ready yet"

   if (str == label_to_find):
      if (tag == "1"):
         player1Score += 1
      elif (tag == "2"):
         player2Score += 1

      active_ = False
      labelUpdate = True
      player1Updated = False
      player2Updated = False

      return "found the right object"
      
   return "found the wrong object\n\n-----\nThe object is: " + label_to_find + "\n-----\n\n"



@app.route("/playerUpdate")
def playerUpdate():
   #global imports
   global random_labels
   global last_label
   global label_to_find
   global active_
   global labelUpdate
   global player1Here
   global player2Here
   global player1Score
   global player2Score
   global player1prev
   global player2prev
   global player1Updated
   global player2Updated
   # globals imports

   if (player1Here == False or player2Here == False): return "Other player isn't ready yet"

   data = 'fail'
   if 'data' in request.args: 
      data = request.args.get('data')

   tag = data[0]

   if (active_ == False):
      active_ = True
      label_to_find = random.choice(random_labels)
      # Prevent duplicate label picking
      while(label_to_find == last_label) :
         label_to_find = random.choice(random_labels)
      last_label = label_to_find
      

   if (tag == "1"):
      if (player1Updated == False):
         if (labelUpdate):
            temp = f"New score is\nPlayer 1: {player1Score}\nPlayer 2: {player2Score}\nNew label to find is: {label_to_find}"
            player1Updated = True
            return temp

   if (tag == "2"):
      if (player2Updated == False):
         if (labelUpdate):
            temp = f"New score is\nPlayer 1: {player1Score}\nPlayer 2: {player2Score}\nNew label to find is: {label_to_find}"
            player2Updated = True
            return temp

   if (player1Updated and player2Updated): labelUpdate = False

   return ""


if __name__ == '__main__':
    app.run()
