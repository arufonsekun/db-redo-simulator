class Transaction:

    def __init__(self, name, tuple_id, column, value):

        self.name = name
        self.tuples_id = [tuple_id]
        self.updates = { column: value }
        self.commited = False
        self.is_in_checkpoint = False


    def add_new_tuple(self, tuple_id, column, value):
        self.tuples_id.append(tuple_id)
        self.updates[column] = value


    def commit(self):
        self.commited = True


    def is_inside_checkpoint(self, is_in):
        self.is_in_checkpoint = is_in
