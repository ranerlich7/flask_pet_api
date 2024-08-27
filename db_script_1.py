import psycopg2
from psycopg2 import sql

# Database connection parameters (update with your Render database details)
DATABASE = {
    'dbname': 'pets_db_fk2z',
    'user': 'pets_db_fk2z_user',
    'password': 'F6wLfd0wmwUnMBZDJ4MgAtVi85pPmQN6',
    'host': 'dpg-cr6uggrtq21c73frjn8g-a.frankfurt-postgres.render.com',
    'port': '5432'
}

def create_table_and_insert_data():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    
    # drop_table_command='''DROP TABLE IF EXISTS pets;'''
    # SQL command to create the 'pets' table
    create_table_command = '''
    CREATE TABLE IF NOT EXISTS pets (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER,
        image TEXT
    );
    '''
    
    # SQL command to insert sample data
    insert_data_command = '''
    INSERT INTO pets (name, age, image) VALUES
    ( 'Dixie', 5, 'https://t4.ftcdn.net/jpg/01/99/00/79/360_F_199007925_NolyRdRrdYqUAGdVZV38P4WX8pYfBaRP.jpg'),
    ( 'Charlie', 2, 'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg')
    ON CONFLICT (id) DO NOTHING;  -- Prevents insertion of duplicate IDs
    '''
    
    try:
        # Create the 'pets' table
        # cur.execute(drop_table_command)
        cur.execute(create_table_command)
        conn.commit()
        print("Table 'pets' created successfully or already exists.")
        
        # Insert sample data into the 'pets' table
        cur.execute(insert_data_command)
        conn.commit()
        print("Sample data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_table_and_insert_data()
