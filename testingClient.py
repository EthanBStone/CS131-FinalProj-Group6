import requests
import time
import threading

tag = "2"
active_ = True

def getUpdate():
   s = tag
   while (active_ == True):
      time.sleep(1.5)
      r = requests.get(f"http://127.0.0.1:5000/playerUpdate?data={s}")
      if (r.text != ""): print(f"Response: {r.text}")


if __name__ == '__main__':
   #s = input("Enter data to send to the server: ")
   #r = requests.get(f"http://127.0.0.1:5000/data?data={s}")
   #print(f"Response: {r.text}")
   tag = input("Say which player you are")
   time.sleep(1)
   s = tag + "here"
   requests.get(f"http://127.0.0.1:5000/playerInput?data={s}")

   t1 = threading.Thread(target=getUpdate)
   t1.start()
   while active_:
      playerinput = input("Enter data to send to the server\n")
      if (playerinput == 'q'): break
      playerinput = tag + playerinput
      r = requests.get(f"http://127.0.0.1:5000/playerInput?data={playerinput}")
      #r = requests.get(f"http://127.0.0.1:5000/playerUpdate?data={tag}")
      if (r.text != ""): print(f"Response: {r.text}")


   active_ = False
   t1.join()

   time.sleep(1)
   requests.get(f"http://127.0.0.1:5000/playerInput?data={s}")