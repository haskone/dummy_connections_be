from http import HTTPStatus

from flask import Blueprint
from webargs.flaskparser import use_args

from connections.models.connection import Connection
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<int:connection_id>', methods=['PUT'])
@use_args(ConnectionSchema(), locations=('json',))
def update_connection(data, connection_id):
    connection = Connection.query.get(connection_id)
    connection.connection_type = data.connection_type
    connection.save()
    # It's arguably whether or not we need to return
    # result body. But let's keep in consistent
    return ConnectionSchema().jsonify(connection), HTTPStatus.OK


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK
