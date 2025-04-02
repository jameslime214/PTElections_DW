import os
import pandas as pd
import psycopg2
from myDataMethods import extract_dataframe_from_excel


def generate_ddl_from_excel(file_path: str) -> tuple[pd.DataFrame, str]:
    """
    Generate SQL Data Definition/Manipulation Language script containing create table statements as well as insertion statemtens from a CSV or Excel file.

    This function reads the provided file (CSV, XLS, or XLSX) into a pandas DataFrame, maps its data types to SQL
    types, and constructs a CREATE TABLE statement along with INSERT commands for each row of data. This facilitates
    an ETL process by generating both the table definition and the corresponding data insertion queries.

    Parameters:
        file_path (str): Full contextual path to the input file (.csv, .xls, or .xlsx).

    Returns:
        tuple: A tuple containing:
            - pandas.DataFrame: The data read from the input file.
            - str: The SQL DDL statement including the table creation and insertion commands.

    Raises:
        ValueError: If the file format is unsupported or if an error occurs during file reading.
    """
    
    ## Extract the file name and extension
    file_name = os.path.basename(file_path)
    base_name, _ = os.path.splitext(file_name)

    ## Read the file into a DataFrame based on its extension using custom method
    df = extract_dataframe_from_excel(file_path)

    ## Define mapping from pandas data types to SQL data types
    dtype_mapping = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }
    
    ## Build a list of column definitions for the CREATE TABLE statement
    columns = []
    for column, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'TEXT')
        columns.append(f'    "{column}" {sql_type}')
    
    ## Construct the CREATE TABLE DDL statement
    ddl = f"CREATE TABLE IF NOT EXISTS {base_name} (\n"
    ddl += ",\n".join(columns)
    ddl += "\n);"
    
    ## Prepare a comma-separated list of column names for the INSERT statements
    columns_list = ", ".join([f'"{col}"' for col in df.columns])
    insert_statements = []
    
    ## Generate an INSERT statement for each row in the DataFrame
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
                ## Escape single quotes in string values by replacing them with two single quotes
                values.append(f"'{str(row[col]).replace('\'', '\'\'')}'")
            else:
                values.append(str(row[col]))
        values_str = ", ".join(values)
        insert_statements.append(f"INSERT INTO {base_name} ({columns_list}) VALUES ({values_str});")
    
    ## Append the INSERT statements to the DDL with a separating newline
    ddl += "\n\n" + "\n".join(insert_statements)
    ddl += "\n"
    
    return df, ddl
    

def save_sql_script(sql_script: str, output_dir: str) -> None:
    """
    Save a SQL script string to a file without overwriting an existing file.
    
    The function assumes that the SQL script begins with the format:
        "CREATE TABLE IF NOT EXISTS {base_name} (\n"
    where base_name is the intended table (and file) name.
    
    Parameters:
        sql_script: The SQL script string to save.
        output_dir: The folder path where the SQL file will be saved.
    """
    ## Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    ## Define the expected prefix and extract the base_name from the SQL script
    prefix = "CREATE TABLE IF NOT EXISTS "
    if not sql_script.startswith(prefix):
        raise ValueError("SQL script does not start with the expected prefix.")
    prefix_len = len(prefix)
    end_index = sql_script.find(" (", prefix_len)
    if end_index == -1:
        raise ValueError("SQL script does not have the expected format.")
    
    ## Create the full output file path (e.g., output_dir/base_name.sql)
    base_name = sql_script[prefix_len:end_index].strip()
    output_file = os.path.join(output_dir, base_name + '.sql')
    
    ## If a file with this name already exists, append an underscore and a counter
    counter = 1
    original_base = os.path.join(output_dir, base_name)
    while os.path.exists(output_file):
        output_file = f"{original_base}_{counter}.sql"
        counter += 1
    
    ## Write the SQL script to the output file
    try:
        with open(output_file, 'w') as f:
            f.write(sql_script)
        saved_filename = os.path.basename(output_file)
        print(f"Successfully saved {saved_filename} to {output_dir}")
    except Exception as e:
        raise ValueError(f"Error writing SQL file: {str(e)}")


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