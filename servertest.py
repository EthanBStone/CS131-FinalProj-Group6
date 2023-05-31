
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

hello_1 = 'hello'


@app.route("/")
def hello_world():
    print(hello_1)
    return "<h1>Home Page</h1>"

@app.route("/data")
def data():
   global hello_1
   hello_1 = "goodbye"
   print(hello_1)
   data = 'fail'
   if 'data' in request.args: 
      data = request.args.get('data')
   return data

if __name__ == '__main__':
    app.run()
