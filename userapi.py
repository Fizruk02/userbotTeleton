from flask import Flask, jsonify, request
import multiprocessing as mp
from teleton import Teleton

app = Flask(__name__)


@app.route('/createChannels', methods=['POST'])
def create():
	tel = Teleton(request.json['api_id'], request.json['api_hash'], request.json['username'], request.json['password'])

	context = mp.get_context('spawn')
	answer = context.Queue()
	new_process = context.Process(target=tel.createChannels, args=( request.json['title'], request.json['group_title'], answer,), daemon=False)
	new_process.start()
	data = answer.get()
	new_process.join()
	return jsonify(data)

@app.route('/editAdmin', methods=['POST'])
def edit():
	tel = Teleton(request.json['api_id'], request.json['api_hash'], request.json['username'], request.json['password'])
	
	context = mp.get_context('spawn')
	answer = context.Queue()
	new_process = context.Process(target=tel.editAdmin, args=(request.json['channel_id'], request.json['group_id'], answer,), daemon=False)
	new_process.start()
	data = answer.get()
	new_process.join()
	return jsonify(data)

if(__name__ == '__main__'):
	app.run(host="45.9.41.117", port=5512)