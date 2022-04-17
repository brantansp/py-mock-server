from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import example

app = Flask(__name__)

# Function call
@app.route('/hello')
def hello():
    return example.add(10, 20)


# Dynamic timestamp call
@app.route('/time')
def times():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%H%M%S")
    return str(uuid.uuid1())


# Sample json call
@app.route('/users/<user_id>', methods=['GET', 'POST'])
def user(user_id):
    if request.method == 'GET':
        return user_id
    if request.method == 'POST':
        content = request.json
        return jsonify(content["data"][0]['id'])
