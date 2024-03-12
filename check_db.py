import sqlite3

def print_table_contents(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Execute a SELECT query to fetch all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Print the column names
        column_names = [description[0] for description in cursor.description]
        print("|".join(column_names))

        # Print the rows
        for row in rows:
            row_values = [str(value) for value in row]
            print("|".join(row_values))

        print()  # Add a blank line between tables

    conn.close()

# Usage example
db_name = "workflow.db"
print_table_contents(db_name)