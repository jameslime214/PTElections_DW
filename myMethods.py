import os
import pandas as pd
import psycopg2

def run_sql_in_server(file_path, _cursor):
    with open(file_path, 'r') as file:
        _cursor.execute(file.read())
    
def read_data_from_table(table_name, _cursor):
    '''
    Read data from the specified table and print it.
    :param table_name: Name of the table to read from
    '''
    _cursor.execute(f"SELECT * FROM {table_name};")
    rows = _cursor.fetchall()
    for row in rows:
        print(row)
    
def iter_file_paths(directory: str):
    """
    Yields the full path for each file in the specified directory.
    
    Parameters:
        directory (str): The path to the directory.
        
    Yields:
        str: The full file path of each file in the directory.
    """
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            yield filepath
    
def generate_ddl_from_file(file_path):
    """
    Generate SQL DDL from a CSV or Excel file
    
    Args:
        file_path (str): Path to the input file (.csv, .xls, or .xlsx)
    
    Returns:
        str: SQL DDL statement
    """
    
    # Extract the file extension using os.path.splitext
    _, ext = os.path.splitext(file_path)
    file_extension = ext.lower()[1:]  # Remove the leading dot

    # Check if the file extension is valid
    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv, .xls, or .xlsx files")

    dtype_mapping = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }
    
    # Use os.path.basename and os.path.splitext to extract the table name
    table_name = os.path.splitext(os.path.basename(file_path))[0].lower()
    columns = []
    for column, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'TEXT')
        columns.append(f'    "{column}" {sql_type}')
    
    # Data table creation DDL
    ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    ddl += ",\n".join(columns)
    ddl += "\n);"
    
    # Data insertion DDL / Extraction step of the ETL process
    columns_list = ", ".join([f'"{col}"' for col in df.columns])
    insert_statements = []
    for index, row in df.iterrows():
        values = []
        for col in df.columns:
            if pd.isna(row[col]):
                values.append('NULL')
            elif isinstance(row[col], (int, float)):
                values.append(str(row[col]))
            elif isinstance(row[col], bool):
                values.append('TRUE' if row[col] else 'FALSE')
            elif isinstance(row[col], str):
                values.append(f"'{row[col].replace('\'', '\'\'')}'")
            else:
                values.append(str(row[col]))
        values_str = ", ".join(values)
        insert_statements.append(f"INSERT INTO {table_name} ({columns_list}) VALUES ({values_str});")
    ddl += "\n\n" + "\n".join(insert_statements)
    ddl += "\n"

    return df, ddl