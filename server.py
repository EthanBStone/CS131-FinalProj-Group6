

from flask import Flask, redirect, url_for, request
import random
#For cloud label generation
# pip install --upgrade google-cloud-storage
#import os
#from google.cloud import storage
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceKeyGCloud.json'
#storage_client = storage.Client()


app = Flask(__name__)

random_labels = ['jersey', 'water_bottle', 'pill_bottle', 'backpack','joystick']
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
playerWon = 0
player1prev = ""
player2prev = ""
player1Updated = False #True
player2Updated = False #True
players = {}


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
   # Player joins game
   if (str == "here"):
      #players[tag] = Player()
      #players[tag].name = tag
      #players[tag].score = 0
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



def playersNotReady() :
     #print("P count = ", len(players))
     return player1Here == False or player2Here == False

def pickNewLabel() :
   global last_label
   global label_to_find
   global random_labels
   # Cloud testing
   #global stoage_client
   #bucket = storage_client.get_bucket('possible_object_labels')
   #blob = storage_client.get_blob('objNames.txt')
   #blob = blob.download_as_string()
   #blob = blob.decode('utf-8')

   #random_labels = []
   #for label in blob.split():
      #random_labels.append(label)
   
   label_to_find = random.choice(random_labels)
   # Prevent duplicate label picking
   while(label_to_find == last_label) : 
      label_to_find = random.choice(random_labels)
   last_label = label_to_find

def winCheck() :
   global player1Score
   global player2Score     
   global max_score

   if player1Score > max_score :
      return 1
   elif player2Score > max_score :
      return 2
   return -1 

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
   global playerWon
   # globals imports

   if (playersNotReady()): return "Other player isn't ready yet"

   data = 'fail'
   if 'data' in request.args: 
      data = request.args.get('data')

   tag = data[0]

   if (active_ == False):
      active_ = True
      pickNewLabel()

   if (tag == "1"):
      if playerWon == 2:
         temp = f"Player 2 wins! Restarting game\nNew label to find is: {label_to_find}"
         playerWon = 0
         player1Updated = True
         return temp
      if (player1Updated == False):
         if (labelUpdate):
            if(winCheck() == 1) :
               temp = f"Player 1 wins! Restarting game\nNew label to find is: {label_to_find}"
               player1Score = 0
               player2Score = 0
               playerWon = 1
            else :
               temp = f"New score is\nPlayer 1: {player1Score}\nPlayer 2: {player2Score}\nNew label to find is: {label_to_find}"
            player1Updated = True

            return temp

   if (tag == "2"):
      if playerWon == 1:
         temp = f"Player 1 wins! Restarting game\nNew label to find is: {label_to_find}"
         playerWon = 0
         player1Updated = True
         return temp      
      if (player2Updated == False):
         if (labelUpdate):
            if(winCheck() == 2) :
               temp = f"Player 2 wins! Restarting game\nNew label to find is: {label_to_find}"
               player1Score = 0
               player2Score = 0
               playerWon == 2           
            else:
               temp = f"New score is\nPlayer 1: {player1Score}\nPlayer 2: {player2Score}\nNew label to find is: {label_to_find}"
            player2Updated = True
            return temp

   if (player1Updated and player2Updated): labelUpdate = False

   return ""


if __name__ == '__main__':
    app.run()
