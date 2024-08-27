from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)

# Initialize CORS
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500",]}})

# Database connection parameters (update with your Render database details)
DATABASE = {
    'dbname': 'pets_db_fk2z',
    'user': 'pets_db_fk2z_user',
    'password': 'F6wLfd0wmwUnMBZDJ4MgAtVi85pPmQN6',
    'host': 'dpg-cr6uggrtq21c73frjn8g-a.frankfurt-postgres.render.com',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE)
    return conn

@app.route('/')
def root():
    return """
    GET /pets - list of pets <br>
    GET /pets/<id> - single pet <br>
    POST /pets - add a pet <br>
    DELETE /pets/<id> - delete a pet <br>
    PUT /pets/<id> - update a pet <br>
"""

@app.route('/pets/', methods=['GET'])
def pets_list():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM pets;')
    pets = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(pets)

@app.route('/pets/', methods=['POST'])
def add_pet():
    try:
        new_pet = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO pets ( name, age, image) VALUES ( %s, %s, %s);',
            ( new_pet['name'], new_pet['age'], new_pet['image'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'result': 'added successfully'}), 201
    except Exception as e:
        print(e)
    return jsonify({'result': 'unexpected error in add'}), 400


@app.route('/pets/<int:id>/', methods=['GET'])
def single_pet(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM pets WHERE id = %s;', (id,))
    pet = cur.fetchone()
    cur.close()
    conn.close()
    
    if pet:
        return jsonify(pet)
    return jsonify({'result': 'Pet not found'}), 404

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM pets WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'result': 'Pet deleted successfully'}), 200

@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    updated_pet = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE pets SET name = %s, age = %s, image = %s WHERE id = %s;',
        (updated_pet['name'], updated_pet['age'], updated_pet['image'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'result': 'Pet updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
