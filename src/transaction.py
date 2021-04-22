class Transaction:

    def __init__(self, name, tuple_id, column, value,
            commited=False, is_succeeded_by_checkpoint=False):

        self.name = name
        self.tuple_id = [tuple_id]
        self.columns = [column]
        self.values = [value]
        self.commited = commited
        self.is_succeeded_by_checkpoint = is_succeeded_by_checkpoint


    def add_new_tuple(self, tuple_id, column, value):
        self.tuple_id.append(tuple_id)
        self.columns.append(column)
        self.values.append(value)