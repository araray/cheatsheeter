# app.py

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import CheatSheet
from config import config
import os

app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app)  # Enable CORS for all routes

# Ensure the cheatsheets directory exists
os.makedirs(app.config['CHEATSHEETS_FOLDER'], exist_ok=True)

@app.route('/api/cheatsheets', methods=['GET'])
def get_cheatsheets():
    cheatsheets = CheatSheet.list_all()
    return jsonify({'cheatsheets': cheatsheets})

@app.route('/api/cheatsheets/<string:name>', methods=['GET'])
def get_cheatsheet(name):
    try:
        cheatsheet = CheatSheet(name).load()
        return jsonify({'name': name, 'data': cheatsheet.data})
    except FileNotFoundError:
        abort(404, description="Cheat sheet not found.")

@app.route('/api/cheatsheets', methods=['POST'])
def create_cheatsheet():
    data = request.get_json()
    name = data.get('name')
    content = data.get('data', {})
    if not name:
        abort(400, description="Cheat sheet name is required.")
    cheatsheet = CheatSheet(name, content)
    cheatsheet.save()
    return jsonify({'message': 'Cheat sheet created successfully.'}), 201

@app.route('/api/cheatsheets/<string:name>', methods=['PUT'])
def update_cheatsheet(name):
    data = request.get_json()
    content = data.get('data', {})
    cheatsheet = CheatSheet(name, content)
    cheatsheet.save()
    return jsonify({'message': 'Cheat sheet updated successfully.'})

@app.route('/api/cheatsheets/<string:name>', methods=['DELETE'])
def delete_cheatsheet(name):
    cheatsheet = CheatSheet(name)
    try:
        cheatsheet.delete()
        return jsonify({'message': 'Cheat sheet deleted successfully.'})
    except FileNotFoundError:
        abort(404, description="Cheat sheet not found.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

