#!/usr/bin/python3
""" View for State object """

from flask import jsonify, request, abort
from models import storage
from datetime import datetime
from models.state import State
import uuid
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves list of all states """
    states = storage.all('State').values()
    list_state = []
    for state in states:
        list_state.append(state.to_dict())
    return jsonify(list_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves States object define by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 'OK'


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create new state """
    response = request.get_json()
    if response is None:
        abort(404, {'Not a JSON'})
    if 'name' not in response:
        abort(404, {'Missing name'})
    state = State(name=response['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), '201'


@app_views.route('/state/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a state """
    state = Storage.get(State, state_id)
    if state is None:
        abort(404)
    Keys = ['id', 'created_at', 'updated_at']
    response = request.get_json()
    for key in response.items():
        if key not in Keys:
            setattr(state, key)
    storage.save()
    return jsonify(state.to_dict()), '200'