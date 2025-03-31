import os
import pandas as pd
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
    

def read_data_from_table(table_name: str, _cursor: psycopg2.extensions.cursor):
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


def iter_file_paths(directory: str):
    """
    Yields the full path for each file in the specified directory.
    
    Parameters:
        directory: The path to the directory.
        
    Yields:
        str: The full file path of each file in the directory.
    """
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            yield filepath
    

def process_txt_file(source_path: str, *, _encoding: str = 'utf-8', has_header: bool = False) -> pd.DataFrame:
    """
    Process a .txt file containing fixed-width formatted data.

    This function performs the following steps:
      - Verifies that the provided file has a .txt extension.
      - Reads the file using pandas.read_fwf to parse fixed-width formatted data.
      - Determines whether the file contains a header row based on the 'has_header' flag.
      - Returns the resulting DataFrame.

    Parameters:
        source_path: Path to the input .txt file.
        _encoding (optional): Encoding to use when reading the file. Default is 'utf-8'.
        has_header (optional): Indicates whether the file contains a header row, defaults to False.
            * True to infer the header row (do not pass the header argument),
            * False to treat the file as raw data (pass header=None).
    
    Returns:
        pandas.DataFrame: The data read from the text file.

    Raises:
        ValueError: If the file extension is not .txt or if an error occurs while reading the file.
    """
    ## Ensure the file has a .txt extension
    if os.path.splitext(source_path)[1].lower() != '.txt':
        raise ValueError("Unsupported file format. This function only processes .txt files.")

    try:
        ## Choose the appropriate header handling based on the has_header flag
        if has_header:
            ## Do not pass the header parameter to let pandas infer the header row
            df = pd.read_fwf(source_path, encoding=_encoding)
        else:
            ## Explicitly specify that there is no header row
            df = pd.read_fwf(source_path, encoding=_encoding, header=None)
    except Exception as e:
        raise ValueError("Error reading fixed-width file: " + str(e))
    
    return df


def parse_FC_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a DataFrame containing municipal or parish data where the first column contains combined numeric + text data (e.g. "123456Municipality Name").
    
    This function splits the first column into two parts:
      - A new leftmost column containing the numeric code.
      - The original first column is replaced with only the non-numeric (text) part.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        pandas.DataFrame: Modified DataFrame with split first column.
    """

    ## Ensure values are treated as strings
    col0 = df[0].astype(str)

    ## Extract numeric part from the first column using a regex
    numeric_part = col0.str.extract(r'^(\d+)')[0]
    ## Extract text part from the first column (trim any whitespace)
    text_part = col0.str.extract(r'^\d+(.*)$')[0].str.strip()
    
    ## Concatenate the extracted numeric part as a new first column, the extracted text part as the next column, then all remaining columns.
    new_df = pd.concat([numeric_part, text_part, df.iloc[:, 1:]], axis=1)
    
    ## Reset column names to default integer indices
    new_df.columns = range(new_df.shape[1])
    
    return new_df


def generate_ddl_from_file(file_path: str) -> tuple[pd.DataFrame, str]:
    """
    Generate SQL Data Definition Language (DDL) statement and insertion commands from a CSV or Excel file.

    This function reads the provided file (CSV, XLS, or XLSX) into a pandas DataFrame, maps its data types to SQL
    types, and constructs a CREATE TABLE statement along with INSERT commands for each row of data. This facilitates
    an ETL process by generating both the table definition and the corresponding data insertion queries.

    Parameters:
        file_path (str): Path to the input file (.csv, .xls, or .xlsx).

    Returns:
        tuple: A tuple containing:
            - pandas.DataFrame: The data read from the input file.
            - str: The SQL DDL statement including the table creation and insertion commands.

    Raises:
        ValueError: If the file format is unsupported or if an error occurs during file reading.
    """
    ## Extract the file extension and convert it to lowercase (remove the leading dot)
    _, ext = os.path.splitext(file_path)
    file_extension = ext.lower()[1:]

    ## Read the file into a DataFrame based on its extension
    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv, .xls, or .xlsx files")

    ## Define mapping from pandas data types to SQL data types
    dtype_mapping = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }
    
    ## Extract the table name from the file path (use the file name without extension, in lowercase)
    table_name = os.path.splitext(os.path.basename(file_path))[0].lower()
    
    ## Build a list of column definitions for the CREATE TABLE statement
    columns = []
    for column, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'TEXT')
        columns.append(f'    "{column}" {sql_type}')
    
    ## Construct the CREATE TABLE DDL statement
    ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
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
                values.append(f"'{row[col].replace('\'', '\'\'')}'")
            else:
                values.append(str(row[col]))
        values_str = ", ".join(values)
        insert_statements.append(f"INSERT INTO {table_name} ({columns_list}) VALUES ({values_str});")
    
    ## Append the INSERT statements to the DDL with a separating newline
    ddl += "\n\n" + "\n".join(insert_statements)
    ddl += "\n"
    
    return df, ddl
