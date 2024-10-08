from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species
        }

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return jsonify(body), 200

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return jsonify(body), status

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = [pet.to_dict() for pet in Pet.query.filter_by(species=species).all()]
    body = {
        'count': len(pets),
        'pets': pets
    }
    return jsonify(body), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
