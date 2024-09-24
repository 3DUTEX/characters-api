import json
from src.contexts.database_context import cursor,conn

table_name = 'characters'

def load(config: dict):
    offset = config.get('offset') or 0
    limit = config.get('limit') or 10

    query = f''' 
        SELECT * FROM "{table_name}"
        ORDER BY "id"
        LIMIT {limit} OFFSET {offset}
    '''

    cursor.execute(query, {})

    rows = cursor.fetchmany(size=limit)

    characters = []
    for row in rows:
        character = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'characteristics': row[3],
            'image_url': row[4],
            'created_at': row[5],
        }
        characters.append(character)

    return characters

def load_by_id(id):
    query = f'SELECT * FROM "{table_name}" WHERE "id" = %s'

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    if not (row):
        return None

    character = {
        'id': row[0],
        'name': row[1],
        'description': row[2],
        'characteristics': row[3],
        'image_url': row[4],
        'created_at': row[5], 
    }

    return character

def create(data: dict):
    query = f'''
        INSERT INTO "{table_name}"
        ("name","description","characteristics","image_url")
        VALUES (%s,%s,%s,%s)
        RETURNING "id"
    '''

    character = (
        data.get('name') or '',
        data.get('description') or '',
        json.dumps(data.get('characteristics') or {}),
        data.get('image_url') or '',
    )

    cursor.execute(query, (character))

    row = cursor.fetchone()

    conn.commit()

    # returning id
    return row[0]
    
def delete(id):
    query = f'DELETE FROM "{table_name}" WHERE "id" = %s'

    cursor.execute(query, (id,))

    conn.commit()

    return id

def update(id, data: dict):
    query = f'''
        UPDATE "{table_name}"
        SET "name" = %s,"description" = %s, "characteristics" = %s,"image_url" = %s
        WHERE "id" = %s
    '''

    current_values = load_by_id(id,)

    if not (current_values):
        raise Exception(f'Character is not find! [ID: {id}]')

    character = (
        data.get('name') or current_values['name'],
        data.get('description') or current_values['description'],
        json.dumps(data.get('characteristics') or current_values['characteristics']),
        data.get('image_url') or current_values['image_url'],
        id, # id
    )

    cursor.execute(query, (character))

    conn.commit()

    new_character = {
        'id': current_values['id'],
        'name': character[0],
        'description': character[1],
        'characteristics': json.loads(character[2]),
        'image_url': character[3],
        'created_at': current_values['created_at']
    }

    return new_character