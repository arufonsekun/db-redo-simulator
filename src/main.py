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

    try:
        with open(log_file, "r") as log:
            t = parser.classify_transactions(log)

            for t_name, t_value in t.items():
                print("------------------------------------")
                print("Transaction name {}".format(t_name))
                print("Transaction tuple_id {}".format(t_value.tuple_id))
                print("Transaction values {}".format(t_value.values))
                print("Transaction columns {}".format(t_value.columns))
                print("Transaction is commited {}".format(t_value.commited))
                print("Transaction is succeeded by CHK_P{}".format(t_value.is_succeeded_by_checkpoint))

            db.close(conn)

    except (Exception, error):
        conn.close()
        raise error

    
if __name__ == "__main__":
    main()

    
