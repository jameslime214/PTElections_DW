import os
import psycopg2


def run_sql_in_server(file_path: str, _cursor: psycopg2.extensions.cursor):
    """
    Run a SQL file in the PostgreSQL server using the provided cursor.
    """
    ## Ensure filetype is .sql
    if os.path.splitext(file_path)[1].lower() != '.sql':
        raise ValueError("Unsupported file format. This function only processes .sql files.")
    else:
        print(f"Running SQL file: {file_path}")
        with open(file_path, 'r') as file:
            _cursor.execute(file.read())
    

def read_table_from_server(table_name: str, _cursor: psycopg2.extensions.cursor):
    """
    Retrieve and print all records from the specified database table.

    This function executes a SQL query to select every record from the table 
    identified by 'table_name'. It then fetches the resulting rows and prints each 
    one to the standard output.

    Parameters:
        table_name: The name of the table from which to retrieve data.
        _cursor: A database cursor object used to execute SQL commands.

    Returns:
        None

    Note:
        Ensure that 'table_name' is a trusted input, as it is directly inserted into the SQL statement.
        For untrusted input, consider using parameterized queries to prevent SQL injection.
    """
    _cursor.execute(f"SELECT * FROM {table_name};")
    rows = _cursor.fetchall()
    for row in rows:
        print(row)