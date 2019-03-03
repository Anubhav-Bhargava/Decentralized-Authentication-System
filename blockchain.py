# Python module imports
import datetime as dt
import hashlib
from flask import Flask, request, render_template, Response

# Importing local functions
from block import *
from genesis import create_genesis_block
from newBlock import next_block, add_block
from getBlock import find_records
from checkChain import check_integrity

# Flask declarations
app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

# Initializing blockchain with the genesis block
blockchain = create_genesis_block()
data = []

# Default Landing page of the app
@app.route('/',  methods = ['GET'])
def index():
    return render_template("index.html")

# Get Form input and decide what is to be done with it
@app.route('/', methods = ['POST'])
def parse_request():
    if(request.form.get("name")):
        while len(data) > 0:
            data.pop()
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template("class.html",
                                name = request.form.get("name"),
                                date = dt.date.today())

    elif(request.form.get("password")):
        while len(data) > 2:
            data.pop()
        data.append(request.form.get("username"))
        data.append(request.form.get("password"))
        add_block(request.form, data, blockchain)
        return "Success: Credentials Added to Blockchain!!"

   
    else:
        return "Invalid POST request. This incident has been recorded."

# Show page to get information for fetching records
@app.route('/view.html',  methods = ['GET'])
def view():
    return render_template("before_view.html")

# Process form input for fetching records from the blockchain
@app.route('/view.html',  methods = ['POST'])
def show_records():
    data = []
    data = find_records(request.form, blockchain)
    if data == -1:
        return "Records not found"
    print ("yes yes")
    print(data)
    return render_template("view.html",
                            name = data[0],
                            username = data[2],
                            password = data[3])

# Show page with result of checking blockchain integrity
@app.route('/result.html',  methods = ['GET'])
def check():
    return render_template("result.html", result = check_integrity(blockchain))

# Start the flask app when program is executed
if __name__ == "__main__":
    app.run()
