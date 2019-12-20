
from flask import Flask, request
import json
import requests
import ast
from model_train import train
import time
import argparse
import sys

app = Flask(__name__)

@app.route('/')
def hello():
	return "Device 1"

@app.route('/sendstatus', methods=['GET'])
def send_status():
	api_url = 'http://localhost:8000/clientstatus'

	data = {'client_id': '8001'}
	print(data)

	r = requests.post(url=api_url, json=data)
	print(r, r.status_code, r.reason, r.text)
	if r.status_code == 200:
		print("yeah")
	
	return "Status OK sent !"

@app.route('/sendmodel')
def send_model():
	file = open("local_model/mod1.npy", 'rb')
	data = {'fname':'model1.npy', 'id':'http://localhost:8001/'}
	files = {
		'json': ('json_data', json.dumps(data), 'application/json'),
		'model': ('model1.npy', file, 'application/octet-stream')
	}

	req = requests.post(url='http://localhost:8000/cmodel', 
						files=files)
	# print(req.text)
	return "Model sent !"

@app.route('/aggmodel', methods=['POST'])
def get_agg_model():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		fname = fname['fname']
		print(fname)

		wfile = open("model_update/"+fname, 'wb')
		wfile.write(file)
			
		return "Model received!"
	else:
		return "No file received!"

@app.route('/modeltrain')
def model_train():
	print("Received request")

	# time.sleep(10)
	train()
	print("Model trained successfully!")
	send_status()
	send_model()
	# get_agg_model()
	return "Model trained successfully!"


def define_and_get_arguments(args=sys.argv[1:]):
    # Parse args
    parser = argparse.ArgumentParser(description="Run websocket server worker.")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
		default=8001,
        help="port number of the websocket server worker, e.g. --port 8777",
    )
    parser.add_argument("--host", type=str, default="localhost", help="host for the connection")
    parser.add_argument(
        "--id", type=str, help="name (id) of the websocket server worker, e.g. --id alice"
    )


    args = parser.parse_args(args=args)
    return args

if __name__ == '__main__':
	
	args = define_and_get_arguments(sys.argv[1:])
	id=args.id
	host=args.host
	port=args.port
	print(port)
	app.run(host=host, port=int(port), debug=False, use_reloader=True)
	# app.run(host='localhost', port=8002, debug=False, use_reloader=True)


















