import mysql.connector

# Parâmetros de conexão
db_config = {
    "host": "localhost",
    "user": "caju",
    "password": "1234",
    "database": "caju"
}

# Dados a serem inseridos
account_data = [
    (100, 200, 300),
    (100, 300, 200),
    (200, 100, 300),
    (200, 300, 100),
    (300, 100, 200),
    (300, 200, 100)
]

try:
    # Conectando ao MySQL
    conn = mysql.connector.connect(**db_config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conn.cursor()

    # Comando SQL para criar a tabela 'accounts'
    create_accounts_table_query = """
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        food DECIMAL(10, 2),
        meal DECIMAL(10, 2),
        cash DECIMAL(10, 2)
    )
    """

    # Criando a tabela 'accounts'
    cursor.execute(create_accounts_table_query)

    # Criando a tabela `transactions`
    create_transactions_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        accountId INT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        merchant VARCHAR(255) NOT NULL,
        mcc INT NOT NULL,
        FOREIGN KEY (accountId) REFERENCES accounts(id)
    );
    """

    cursor.execute(create_transactions_table_query)

    insert_query = "INSERT INTO accounts (food, meal, cash) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, account_data)

    conn.commit()

except mysql.connector.Error as err:
    print(f"Erro: {err}")

finally:
    cursor.close()
    conn.close()
