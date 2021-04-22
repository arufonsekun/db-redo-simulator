import re
from .transaction import Transaction


UPDATE = 4
COMMIT = "commit"
CHECKPOINT = "ckpt"
START = "start"


def get_columns_names_and_values(log):
    """Parse the first line of the given
    log file, extracting column name and
    respective value.

    Args:
        log_file (str): path to log file

    Returns:
        dict[str:str]: python dictionary
        following the format → column_name : value
    """
    table_schema = log.readline()

    raw_column_value = table_schema.split("|")

    column_value = [
        tuple(_.split("=")) for _ in raw_column_value
    ]

    column_value = {
        k.lstrip(): v.rstrip() for (k, v) in column_value
    }

    return column_value


def get_inst_content(line):
    """Gets a log file instruction and
    returns content inside "<" and ">".

    Args:
        line (str): log file line

    Returns:
        str: string between "<" and ">"
    """
    content = re.match(r'\<(.*?)\>', line).group(1)
    return content


def get_tokens(instruction):
    """Given an instruction, `get_tokens` generates
    tokens for it.

    Example: 
        <start T1>     → ['start', 'T1']
        <T1, 1, A, 20> → ['T1', '1', 'A', '20']
    
    Args:
        instruction (str): log file instruction.

    Returns:
        list(str): tokens for that compose that 
        instruction.
    """
    tokens = instruction.split(" ")

    is_update_like = len(tokens) == 1
    if is_update_like:
        return tokens[0].split(",")

    return tokens


def is_update(tokens):
    """Tells if the given list of tokens is
    representing an update instruction i.e.
    <T1,1,A,20> or something else: <start T2>,
    <commit T2> or <Start CKPT(T7)>, for instance.

    Args:
        tokens (list(str)): list of tokens.

    Returns:
        boolean: whether or not the given token is representing
        an update instruction.
    """
    return len(tokens) == UPDATE


def is_commit(tokens):
    """Returns whether a list of tokens
    are a commit. 

    Args:
        tokens (list): list of tokens

    Returns:
        boolean: list of token is a commit
    """
    return tokens[0].lower() == COMMIT


def is_start_checkpoint(tokens):
    """Verifies if a given list of
    tokens is start of a checkpoint.

    Args:
        tokens ([type]): [description]

    Returns:
        boolean: is checkpoint start?
    """
    is_start = tokens[0].lower() == START
    is_checkpoint = tokens[1].lower().find(CHECKPOINT) >= 0

    return is_start and is_checkpoint


def is_end_checkpoint(tokens):
    """Verifies if a given list of
    tokens is end of a checkpoint.

    Args:
        tokens ([type]): [description]

    Returns:
        boolean: is checkpoint end?
    """
    is_end = not (tokens[0].lower() == START)
    is_checkpoint = tokens[1].lower().find(CHECKPOINT) >= 0

    return is_end and is_checkpoint

def transaction_already_exists(transactions, t_name):
    """Check if the transaction was previously created.

    Args:
        transactions (dict): transactions dictionary.
        t_name (str): transaction name.

    Returns:
        boolean: check if the transaction was already created.
    """
    return t_name in transactions.keys()


def set_transactions_inside_checkpoint(transactions):
    """Set each transaction as "inside" checkpoint.

    Args:
        transactions (dict): transactions
    """
    for t_name, transaction in transactions.items():
        if transactions[t_name].commited:
            transactions[t_name].is_inside_checkpoint(True)


def classify_transactions(log):
    """Tokenizes log file instructions
    and checks if each transaction is
    commited or inside checkpoint.

    Args:
        log (TextIOWrapper): log file.

    Returns:
        dict: Dictionary of transactions
    """
    transactions = {}
    log_lines = [l.rstrip() for l in log.readlines()[1:]]

    for line in log_lines:
        instruction = get_inst_content(line)
        tokens = get_tokens(instruction)
        
        if is_update(tokens):
            transaction_name = tokens[0]
            tuple_id = tokens[1]
            column = tokens[2]
            value = tokens[3]
        
            if transaction_already_exists(transactions, transaction_name):
                transactions[transaction_name].add_new_tuple(tuple_id, column, value)

            else:
                transaction = Transaction(transaction_name, tuple_id, column, value)
                transactions[transaction_name] = transaction

        elif is_commit(tokens):
            t_name = tokens[1]
            transactions[t_name].commit()

        # TODO: check if it's make sense
        elif is_start_checkpoint(tokens):
            is_inside_checkpoint = True

        elif is_end_checkpoint(tokens):
            set_transactions_inside_checkpoint(transactions)
            is_inside_checkpoint = False

    return transactions


def tokenizer(log):
    """Gets a log file and converts each
    transaction in the format <T1, 1, A, 10>
    into an object. This method is just used
    for testing.

    Args:
        log (file): Log file

    Returns:
        dict: Dictionary associating transactions name
        and object.
    """
    transactions = {}
    log_lines = [l.rstrip() for l in log.readlines()[1:]]
    
    for line in log_lines:
        instruction = get_inst_content(line)
        tokens = get_tokens(instruction)
        
        if is_update(tokens):
            transaction_name = tokens[0]
            tuple_id = tokens[1]
            column = tokens[2]
            value = tokens[3]
        
            if transaction_already_exists(transactions, transaction_name):
                transactions[transaction_name].add_new_tuple(tuple_id, column, value)

            else:
                transaction = Transaction(transaction_name, tuple_id, column, value)
                transactions[transaction_name] = transaction

    return transactions