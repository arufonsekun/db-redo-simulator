import psycopg2
from configparser import ConfigParser


def get_db_config(db_config_file="db-redo-simulator/database.ini",  section="postgres"):
    """[summary]

    Args:
        db_config_file (str, optional): [description]. 
        Defaults to "database.ini".
        section (str, optional): [description]. Defaults to "postgres".

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
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
    """[summary]

    Returns:
        [type]: [description]
    """
    db_config = get_db_config()
    return psycopg2.connect(**db_config)


def close(conn):
    """[summary]

    Args:
        conn ([type]): [description]
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
        print("Table created sucessfuly")

    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        raise error


def drop(conn, table_name):
    """[summary]

    Args:
        conn ([type]): [description]
        table_name ([type]): [description]

    Raises:
        error: [description]
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
    """[summary]

    Args:
        conn ([type]): [description]
        table_name (str): [description]
        columns ([type]): [description]
        values ([type]): [description]

    Raises:
        error: [description]
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
    """[summary]

    Args:
        conn ([type]): [description]
        table_name ([type]): [description]
        columns ([type]): [description]
        values ([type]): [description]

    Raises:
        error: [description]
    """
    update =  "UPDATE {0} SET "
    update = update.format(table_name)

    for column, value in zip(columns, values):
        update += ("{} = {}, ").format(column, value)
    
    update = update[:-2]
    update += " WHERE id=1;"
    print(update)

    try:
        cursor = conn.cursor()
        cursor.execute(update)
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

