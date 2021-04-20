import argparse
from decouple import config

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


if __name__ == "__main__":
    args = get_cmd_args()
    print(args.log)

    
