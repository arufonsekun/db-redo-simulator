import argparse
from ..src import db
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
    conn = db.connect()

    column_value = log_parser.get_columns_names_and_values(args.log)
    db.create(conn, "test", column_value.keys())

    conn.close()


def drop_table_test():
    conn = db.connect()
    db.drop(conn, "test")
    conn.close()


def insert_into_test():
    column_value = log_parser.get_columns_names_and_values(args.log)

    print("Columns name: {}".format(column_value.keys()))
    print("Columns values: {}".format(column_value.values()))
    
    conn = db.connect()
    
    columns = column_value.keys()
    values = column_value.values()
    db.insert(conn, "test", tuple(columns), tuple(values))
    
    conn.close()


def update_table_test():
    conn = db.connect()
    db.update(conn, "test", ('A', 'C'), (4, 5))
    conn.close()


if __name__ == "__main__":
    args = get_cmd_args()
    print("Log file path: {}".format(args.log))

    # parse_table_schema(args)
    # create_table_test(args)
    # insert_into_test()
    # drop_table_test()
    update_table_test()



    