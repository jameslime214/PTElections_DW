import os
import numpy as np
import pandas as pd

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
    
def process_txt_file(source_path:str, *, _encoding='utf-8'):
    """
    Process a .txt file with fixed-width formatted data.
    This function:
    - Checks that the source file has a .txt extension.
    - Reads the file using pandas.read_fwf to parse the fixed-width format, with the provided encoding.
    - Returns the resulting DataFrame.

    Parameters:
        source_path (str): Path to the input .txt file.
        target_dir (str): Path to the directory where the output .xlsx file will be saved.
        _encoding (kwarg, str): Encoding to use when reading the file. Default is 'utf-8'.
    
    Returns:
        pandas.DataFrame: The data read from the txt file.

    Raises:
        ValueError: If the file extension is not .txt or if there is an error reading the file.
    """

    ## Ensure the file is a .txt file
    if os.path.splitext(source_path)[1].lower() != '.txt':
        raise ValueError("Unsupported file format. This function only processes .txt files.")

    try:
        ## Read the txt file using read_fwf which auto-detects fixed-width columns
        df = pd.read_fwf(source_path, encoding=_encoding, header=None)
    except Exception as e:
        raise ValueError("Error reading fixed-width file: " + str(e))

    return df

def parse_FC_data(df):
    """
    Process a DataFrame containing municipal data where the first column contains combined numeric + text data (e.g. "123456Municipality Name").
    
    This function splits the first column into two parts:
      - A new leftmost column containing the numeric code.
      - The original first column is replaced with only the non-numeric (text) part.
    
    Args:
        df (pandas.DataFrame): Input DataFrame.
        
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
    new_df = pd.concat([numeric_part.astype('int64'), text_part, df.iloc[:, 1:]], axis=1)
    
    ## Reset column names to default integer indices
    new_df.columns = range(new_df.shape[1])
    
    return new_df

def generate_ddl_from_file(file_path):
    """
    Generate SQL DDL from a CSV or Excel file
    
    Args:
        file_path (str): Path to the input file (.csv, .xls, or .xlsx)
    
    Returns:
        str: SQL DDL statement
    """
    
    ## Extract the file extension using os.path.splitext
    _, ext = os.path.splitext(file_path)
    file_extension = ext.lower()[1:]  # Remove the leading dot

    ## Check if the file extension is valid
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
    
    ## Use os.path.basename and os.path.splitext to extract the table name
    table_name = os.path.splitext(os.path.basename(file_path))[0].lower()
    columns = []
    for column, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'TEXT')
        columns.append(f'    "{column}" {sql_type}')
    
    ## Data table creation DDL
    ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    ddl += ",\n".join(columns)
    ddl += "\n);"
    
    ## Data insertion DDL / Extraction step of the ETL process
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