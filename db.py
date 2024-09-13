import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            contact VARCHAR(15),
            address VARCHAR(20)
        )
        """
        self.cursor.execute(create_table_query)

    def insert(self, name, age, contact, address):
        insert_query = """
        INSERT INTO employees (name, age, contact, address)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, (name, age, contact, address))
        self.connection.commit()

    def fetch(self):
        fetch_query = "SELECT * FROM employees"
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()

    def update(self, emp_id, name, age, contact, address):
        update_query = """
        UPDATE employees
        SET name = %s, age = %s, contact = %s, address = %s
        WHERE id = %s
        """
        self.cursor.execute(update_query, (name, age, contact, address, emp_id))
        self.connection.commit()

    def remove(self, emp_id):
        delete_query = "DELETE FROM employees WHERE id = %s"
        self.cursor.execute(delete_query, (emp_id,))
        self.connection.commit()

    def __del__(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
