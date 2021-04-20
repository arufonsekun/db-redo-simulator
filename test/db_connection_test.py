import argparse
from ..src import db_connection
from ..src import parser as log_parser


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


def parse_table_schema(args):
    column_value = log_parser.get_columns_names_and_values(args.log)
    print("Columns name: {}".format(column_value.keys()))
    print("Columns values: {}".format(column_value.values()))

def create_table_test(args):
    conn = db_connection.connect()

    column_value = log_parser.get_columns_names_and_values(args.log)
    db_connection.create_table(conn, "test", column_value.keys())

    conn.close()

def drop_table_test():
    conn = db_connection.connect()
    db_connection.drop_table(conn, "test")
    conn.close()

if __name__ == "__main__":
    args = get_cmd_args()
    print("Log file path: {}".format(args.log))

    # parse_table_schema(args)
    # create_table_test(args)

    drop_table_test()


    