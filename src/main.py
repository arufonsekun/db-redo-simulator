import argparse
from . import parser
from . import db

TABLE_NAME = "redo_simulator"


def get_cmd_args():
    """Function used to return command line
    arguments, by now log file path.

    Returns:
        argparse.Namespace: Contains command line arguments
    """

    parser = argparse.ArgumentParser(description="Database redo simulator")
    parser.add_argument(
            "--log", type=str, dest="log",
            help="Database log file")

    arguments = parser.parse_args()

    return arguments


def create_table(conn, columns_values):
    columns = tuple(columns_values.keys())
    values = tuple(columns_values.values())

    db.create(conn, TABLE_NAME, columns)
    db.insert(conn, TABLE_NAME, columns, values)


def drop_table(conn):
    """Drop database table

    Args:
        conn (connection): Postgres object connection
    """
    db.drop(TABLE_NAME)


def main():
    args = get_cmd_args()
    log_file = args.log
    conn = db.connect()
    print(type(conn))

    try:
        with open(log_file, "r") as log:
            columns_values = parser.get_columns_names_and_values(log)
            
            create_table(conn, columns_values)
            db.close(conn)

    except Exception:
        conn.close()

    
if __name__ == "__main__":
    main()

    
