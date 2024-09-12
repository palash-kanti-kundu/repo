import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        columns: a dict where key is column name and value is column type
        """
        columns_str = ', '.join([f'{name} {type}' for name, type in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});")

    def insert_data(self, table_name, data):
        """
        data: a dict where key is column name and value is data to insert
        """
        columns_str = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        self.cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});", list(data.values()))
        self.conn.commit()

    def close(self):
        self.conn.close()