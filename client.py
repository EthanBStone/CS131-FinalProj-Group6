import requests


if __name__ == '__main__':
   s = input("Enter data to send to the server: ")
   r = requests.get(f"http://127.0.0.1:5000/data?data={s}")
   print(f"Response: {r.text}")