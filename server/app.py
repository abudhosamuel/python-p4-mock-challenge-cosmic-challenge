#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Scientist, Planet, Mission
import os

# Set up Flask application and database connection
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Welcome to the Interplanetary Space Travel Agency API!'

# GET /scientists
@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    return jsonify([scientist.to_dict(only=('id', 'name', 'field_of_study')) for scientist in scientists]), 200

# GET /scientists/<int:id>
@app.route('/scientists/<int:id>', methods=['GET'])
def get_scientist(id):
    scientist = Scientist.query.get(id)
    if scientist:
        return jsonify(scientist.to_dict(only=('id', 'name', 'field_of_study', 'missions'))), 200
    else:
        return jsonify({"error": "Scientist not found"}), 404

# POST /scientists
@app.route('/scientists', methods=['POST'])
def create_scientist():
    data = request.get_json()
    try:
        scientist = Scientist(name=data['name'], field_of_study=data['field_of_study'])
        db.session.add(scientist)
        db.session.commit()
        return jsonify(scientist.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

# PATCH /scientists/<int:id>
@app.route('/scientists/<int:id>', methods=['PATCH'])
def update_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    
    data = request.get_json()
    try:
        if 'name' in data:
            scientist.name = data['name']
        if 'field_of_study' in data:
            scientist.field_of_study = data['field_of_study']
        db.session.commit()
        return jsonify(scientist.to_dict()), 202
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

# DELETE /scientists/<int:id>
@app.route('/scientists/<int:id>', methods=['DELETE'])
def delete_scientist(id):
    scientist = Scientist.query.get(id)
    if scientist:
        db.session.delete(scientist)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Scientist not found"}), 404

# GET /planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict(only=('id', 'name', 'distance_from_earth', 'nearest_star')) for planet in planets]), 200

# POST /missions
@app.route('/missions', methods=['POST'])
def create_mission():
    data = request.get_json()
    try:
        mission = Mission(
            name=data['name'],
            scientist_id=data['scientist_id'],
            planet_id=data['planet_id']
        )
        db.session.add(mission)
        db.session.commit()
        return jsonify(mission.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
