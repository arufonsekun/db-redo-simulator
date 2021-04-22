import argparse
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


def test_tokenizer(args):
    log_file = args.log
    try:
        with open(log_file, "r") as log:
            
            t = log_parser.classify_transactions(log)

            for t_name, t_value in t.items():
                print("------------------------------------")
                print("Transaction name {}".format(t_name))
                print("Transaction is commited {}".format(t_value.commited))
                print("Transaction is in checkpoint {}".format(t_value.is_in_checkpoint))

    except (Exception, error):
        raise error


if __name__ == "__main__":
    args = get_cmd_args()
    print("Log file path: {}".format(args.log))
    
    test_tokenizer(args)