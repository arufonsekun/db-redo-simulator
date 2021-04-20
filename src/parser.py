def get_columns_names_and_values(log_file):
    """Parse the first line of the given
    log file, extracting column name and
    respective value.

    Args:
        log_file (str): path to log file

    Returns:
        dict[str:str]: python dictionary
        following the format → column_name : value
    """
    log = open(log_file, "r")
    table_schema = log.readline()
    log.close()

    raw_column_value = table_schema.split("|")

    column_value = [
        tuple(_.split("=")) for _ in raw_column_value
    ]

    column_value = {
        k.lstrip(): v.rstrip() for (k, v) in column_value
    }

    return column_value
