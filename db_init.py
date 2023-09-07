import mysql.connector

# Parâmetros de conexão
db_config = {
    "host": "localhost",
    "user": "caju",
    "password": "1234",
    "database": "caju"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro na conexão com o banco de dados: {err}")
        return None

def getAccountBalanceByMCC(accountId, mcc):
    with get_connection() as conn:
        cursor = conn.cursor()
        query = f"SELECT {mcc} FROM accounts WHERE id = {accountId}"
        cursor.execute(query)
        balance = cursor.fetchone()
        return balance[0] if balance else None
    
def setAccountBalance(accountId, mcc, ammount):
    try: 
        conn = get_connection()
        cursor = conn.cursor()

        query = f"UPDATE accounts SET {mcc} = {ammount} WHERE id = {accountId}"
        cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar o saldo da conta: {err}")
    finally:
        cursor.close()
        conn.close()
    

def create_accounts_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        create_accounts_table_query = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            food DECIMAL(10, 2),
            meal DECIMAL(10, 2),
            cash DECIMAL(10, 2)
        )
        """

        cursor.execute(create_accounts_table_query)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar a tabela de contas: {err}")
    finally:
        cursor.close()
        conn.close()

def create_transactions_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        create_transactions_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            accountId INT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            merchant VARCHAR(255) NOT NULL,
            mcc INT NOT NULL,
            FOREIGN KEY (accountId) REFERENCES accounts(id)
        );
        """

        cursor.execute(create_transactions_table_query)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar a tabela de transações: {err}")
    finally:
        cursor.close()
        conn.close()

def insert_account_data(account_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        insert_query = "INSERT INTO accounts (food, meal, cash) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, account_data)

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao inserir dados de conta: {err}")
    finally:
        cursor.close()
        conn.close()

def main():
    create_accounts_table()
    create_transactions_table()

    # Dados a serem inseridos
    account_data = [
        (100, 200, 300),
        (100, 300, 200),
        (200, 100, 300),
        (200, 300, 100),
        (300, 100, 200),
        (300, 200, 100)
    ]

    insert_account_data(account_data)

if __name__ == "__main__":
    main()
