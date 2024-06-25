import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tools_rental.db')
    conn.row_factory = sqlite3.Row
    return conn

def delete_duplicates():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL para deletar registros duplicados
    sql_delete_duplicates = '''
    DELETE FROM tools
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM tools
        GROUP BY name
    )
    '''

    cursor.execute(sql_delete_duplicates)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    delete_duplicates()
