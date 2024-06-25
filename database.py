import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tools_rental.db')
    conn.row_factory = sqlite3.Row
    return conn

def tool_exists(cursor, name):
    cursor.execute("SELECT id FROM tools WHERE name = ?", (name,))
    return cursor.fetchone() is not None

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        address TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        is_manager BOOLEAN NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        available BOOLEAN NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_date TEXT NOT NULL,
        delivery_date TEXT,
        return_date TEXT,
        status TEXT NOT NULL,
        client_id INTEGER NOT NULL,
        manager_id INTEGER,
        tool_id INTEGER NOT NULL,
        FOREIGN KEY(client_id) REFERENCES users(id),
        FOREIGN KEY(manager_id) REFERENCES users(id),
        FOREIGN KEY(tool_id) REFERENCES tools(id)
    )
    ''')

    # Inserir dados de exemplo na tabela tools se não existirem
    tools_to_insert = [
        ('Martelo', 'Martelo de aço forjado, com cabo de madeira.', 1),
        ('Chave de Fenda', 'Chave de fenda phillips, tamanho médio.', 1),
        ('Serrote', 'Serrote para madeira, 20 polegadas.', 1),
        ('Furadeira', 'Furadeira BOSCH 110v.', 1),
        ('Alicate', 'Alicate de uso geral para diversas aplicações.', 1),
        ('Esmerilhadeira', 'Esmerilhadeira elétrica para corte e desbaste de materiais.', 1),
        ('Lavadora de Alta Pressão', 'Lavadora de alta pressão para limpeza eficiente.', 1),
        ('Esmeril', 'Esmeril para afiação e polimento de materiais.', 1),
        ('Parafusadeira', 'Parafusadeira elétrica para fixação de parafusos.', 1)
    ]

    for tool in tools_to_insert:
        if not tool_exists(cursor, tool[0]):
            cursor.execute("INSERT INTO tools (name, description, available) VALUES (?, ?, ?)", tool)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
