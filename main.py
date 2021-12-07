from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/compare/*": {"origins": "*"}})


def get_database():
    CONNECTION_STRING = "mongodb+srv://admin:admin@webiot.dkgkv.mongodb.net/WebIOT?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    return client['WebIOT']


steps_db = get_database()

steps_collection = steps_db['Steps']


@app.route('/stepsTaken', methods=['GET'])
def get_steps():
    steps_query = {'client_name': 'semaphore'}
    result = steps_collection.find(steps_query)
    steps = 0

    if any(s['client_name'] == 'semaphore' for s in result):
        result.rewind()
        steps_dict = result.next()
        return str(steps_dict['steps'])
    else:
        return str(steps)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)