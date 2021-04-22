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
            help="Database redo simulator.")

    parser.add_argument(
            "--drop", type=bool, dest="drop", nargs='?', const=True,
            help="Should or not drop table after running.")

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


def redo_update(conn, transactions):
    
    for transaction in transactions.values():
        
        columns = tuple(transaction.updates.keys())
        values = tuple(transaction.updates.values())
        print(" ")

        if transaction.commited and transaction.is_in_checkpoint:
            db.update(conn, TABLE_NAME, columns, values)
            print("Transação {} não realizou redo".format(transaction.name))

        elif transaction.commited and not transaction.is_in_checkpoint:
            db.update(conn, TABLE_NAME, columns, values)
            print("Transação {} realizou redo".format(transaction.name))

        else:
            print("Transação {} foi perdida ;(".format(transaction.name))


def show_updated_values(conn):
    current_values = db.select(conn, TABLE_NAME)
    print(current_values)


def main():
    args = get_cmd_args()
    log_file = args.log
    must_drop_table = args.drop

    try:
        with open(log_file, "r") as log:
            conn = db.connect()
            columns_values = parser.get_columns_names_and_values(log)
            create_table(conn, columns_values)

            transactions = parser.classify_transactions(log)
            redo_update(conn, transactions)
            show_updated_values(conn)

            if must_drop_table:
                drop_table(conn)

            conn.close()

    except:
        conn.close()
        raise

    
if __name__ == "__main__":
    main()

    
