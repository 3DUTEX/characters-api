from flask import Blueprint, jsonify, request

from src.repositories import characters_repository
from src.services import characters_services

characters_route = Blueprint('characters_route', __name__)

@characters_route.get('/')
def get():
    offset = request.args.get('offset') or 0
    limit = request.args.get('limit') or 10

    query_config = {
        'offset': int(offset),
        'limit': int(limit)
    }

    characters = characters_repository.load(query_config)
    return jsonify({'data': characters, 'success': True, 'pagination': query_config}), 200

@characters_route.get('/<id>')
def get_by_id(id):
    character = characters_repository.load_by_id(id)
    
    if not (character):
        return jsonify(), 204

    return jsonify({'success': True, 'data': character}), 200

@characters_route.post('/')
def post():
    req_data = request.json
    id = characters_repository.create(req_data)

    if not (id):
        raise Exception('Error in create character!')

    return jsonify({'success': True, 'id': int(id) }), 201

@characters_route.delete('/<id>')
def delete(id):
    id = characters_services.delete(id)
    return jsonify({'success': True, 'id': int(id)}), 200

@characters_route.put('/<id>')
def update(id):
    req_data = request.json

    new_character = characters_repository.update(id, req_data)

    return jsonify({'success': True, 'data': new_character}), 200

@characters_route.patch('/image/<id>')
def patch_image(id):
    file = request.files.get('image')
    
    if not file:
        raise Exception('Error on upload image!')

    file_buffer = file.read()  # get buffer
 
    new_character = characters_services.patch_image(id, file_buffer)

    return jsonify({'success': True, 'data': new_character}), 200