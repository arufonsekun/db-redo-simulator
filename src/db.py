import psycopg2
from configparser import ConfigParser


def get_db_config(db_config_file="db-redo-simulator/database.ini",
    section="postgres"):
    """Get user database configurations. 

    Args:
        db_config_file (str, optional): [description]. 
        Defaults to "database.ini".
        section (str, optional): [description]. Defaults to "postgres".

    Raises:
        Exception: [description]

    Returns:
        dict: database settings.
    """
    parser = ConfigParser()
    parser.read(db_config_file)

    db_config = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        exception = "Database section {0} not found in the {1} file"
        raise Exception(exception.format(section, db_config_file))

    return db_config


def connect():
    """Create a new db connection.

    Returns:
        connection: database connection
    """
    db_config = get_db_config()
    return psycopg2.connect(**db_config)


def close(conn):
    """Close database connection

    Args:
        conn (connection): Database connection.
    """
    conn.close()


def create(conn, table_name, columns):
    """Create a database table given a name
    and a list of columns names, columns types
    are by default integers.    

    Args:
        conn ([type]): database connection
        table_name (str): table name to be created
        columns ([str]): list of columns names

    Returns:
        [type]: [description]
    """
    create =  "CREATE TABLE {0} (\n\tid SERIAL,\n"
    create = create.format(table_name)

    for column in columns:
        create += ("\t{} INTEGER,\n").format(column)
    
    create = create[:-2]
    create += ");"

    try:
        cursor = conn.cursor()
        cursor.execute(create)
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        raise error


def drop(conn, table_name):
    """Drop db table.

    Args:
        conn (connection): db connection.
        table_name (string): table name.

    Raises:
        error: SQL error.
    """
    drop = "DROP TABLE {};".format(table_name)

    try:
        cursor = conn.cursor()
        cursor.execute(drop)
        cursor.close()
        conn.commit()
        print("Table {} dropped sucessfuly".format(table_name))

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

def insert(conn, table_name, columns, values):
    """Insert data into table_name.

    Args:
        conn (connection): active database connection.
        table_name (str): table name.
        columns (tuple): columns to be modified.
        values (tuple): columns values.

    Raises:
        error: SQl error.
    """
    insert = "INSERT INTO {0} {1} VALUES {2};"
    insert = insert.format(table_name, columns, values)
    insert = insert.replace("'", "")

    try:
        cursor = conn.cursor()
        cursor.execute(insert)
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        raise error


def update(conn, table_name, columns, values):
    """Updates table_name data.

    Args:
        conn (connection): database active connection.
        table_name (str): table where data will be inserterd. 
        columns (tuple): columns names
        values (tuple): new columns values.

    Raises:
        error: [description]
    """
    update =  "UPDATE {0} SET "
    update = update.format(table_name)

    for column, value in zip(columns, values):
        update += ("{} = {}, ").format(column, value)
    
    update = update[:-2]
    update += " WHERE id=1;"

    try:
        cursor = conn.cursor()
        cursor.execute(update)
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

def select(conn, table_name, id=1):
    """Select data from table_name
    where id is equal to 1.

    Args:
        conn (connection): database active connection.
        table_name (str): [description]
        id (int, optional): Tuple id where data will be
        retrieved. Defaults to 1.

    Raises:
        error: SQL error

    Returns:
        [type]: [description]
    """
    select = "SELECT * from {0} WHERE id = {1};".format(table_name, id)

    cursor = conn.cursor()
    cursor.execute(select)
    result = cursor.fetchall()
    cursor.close()

    return result

