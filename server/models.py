from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData  # Import MetaData correctly
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Correct metadata setup
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create MetaData object
metadata = MetaData(naming_convention=convention)

# Pass MetaData object to SQLAlchemy
db = SQLAlchemy(metadata=metadata)

# Define your models
class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance_from_earth = db.Column(db.Integer, nullable=False)
    nearest_star = db.Column(db.String, nullable=False)

    # Relationship with Mission
    missions = db.relationship('Mission', backref='planet', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-missions.planet',)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    # Relationship with Mission
    missions = db.relationship('Mission', backref='scientist', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-missions.scientist',)

    # Validation
    @validates('name', 'field_of_study')
    def validate_scientist(self, key, value):
        if not value:
            raise ValueError(f'{key} cannot be empty')
        return value

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    # Serialization rules
    serialize_rules = ('-scientist.missions', '-planet.missions')

    # Validation
    @validates('name', 'scientist_id', 'planet_id')
    def validate_mission(self, key, value):
        if not value:
            raise ValueError(f'{key} cannot be empty')
        return value
