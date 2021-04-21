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
