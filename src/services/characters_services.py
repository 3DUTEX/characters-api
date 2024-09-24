import re
from uuid import uuid4

from src.providers.bucket_provider import client
from src.repositories import characters_repository

bucket_name = 'characters_image'

ext_image = 'jpg'

def delete(id):
        current_character = characters_repository.load_by_id(id)

        if not (current_character):
            raise Exception(f'Character is not finded! [ID: {id}]')

        character_name = current_character['name']

        file_name = _generate_file_name(id, character_name) # generate file name
    
        if (current_character['image_url'] is not ''):
            _remove_file(file_name)

        return characters_repository.delete(id)

def patch_image(id, file_buffer):
    current_character = characters_repository.load_by_id(id)

    if not (current_character):
        raise Exception(f'Character is not finded! [ID: {id}]')
    
    character_name = current_character['name']

    file_name = _generate_file_name(id, character_name) # generate file name

    if not (current_character):
        raise Exception(f'Character is not finded! [ID: {id}]')
    
    if (current_character['image_url'] is not ''):
        _remove_file(file_name)

    # upload in storage
    response = _upload_file(file_name, file_buffer)

    if not (response.status_code is 200):
        raise Exception('Error on upload image!')

    url = _get_url(file_name)

    if not (url):
        raise Exception('Error on retrieve url image!')

    # updating in database
    new_character = characters_repository.update(id, {'image_url': url})

    return new_character

def _remove_file(file_name):
        try:
            client.storage.from_(bucket_name).remove(file_name)
        except Exception as e:
            print(str(e))

def _upload_file(file_name, file_buffer):
     return client.storage.from_(bucket_name).upload(file_name, file_buffer, file_options={'content-type':f'image/{ext_image}'})

def _get_url(file_name):
     return client.storage.from_(bucket_name).get_public_url(file_name)

def _generate_file_name(id, character_name):
    generated_name = f'{id}_{character_name}.{ext_image}';
    cleaned_name = re.sub(r'[^a-zA-Z0-9._]', '', generated_name)
    return cleaned_name