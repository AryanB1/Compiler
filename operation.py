class Operations:
    def __init__(self, type, var):
        self.type = type  # Initialize operation type (e.g., "INT", "FLT")
        self.var = var    # Initialize operation variable (specific value)

    def __repr__(self):
        return str(self.var)


class Integer(Operations):
    def __init__(self, var):
        super().__init__("INT", var)  # Initialize Integer operation with type "INT"


class Float(Operations):
    def __init__(self, var):
        super().__init__("FLT", var)  # Initialize Float operation with type "FLT"


class Operation(Operations):
    def __init__(self, var):
        super().__init__("OP", var)  # Initialize generic Operation with type "OP"


class Declaration(Operations):
    def __init__(self, var):
        super().__init__("DECL", var)  # Initialize Declaration operation with type "DECL"


class Variable(Operations):
    def __init__(self, var):
        super().__init__("VAR(?)", var)  # Initialize Variable operation with type "VAR"


class Boolean(Operations):
    def __init__(self, var):
        super().__init__("BOOL", var)  # Initialize Boolean operation with type "BOOL"


class Comparison(Operations):
    def __init__(self, var):
        super().__init__("COMP", var)  # Initialize Comparison operation with type "COMP"


class Reserved(Operations):
    def __init__(self, var):
        super().__init__("RSV", var)  # Initialize Reserved operation with type "RSV"


class Data:
    def __init__(self):
        self.variable = {}  # Initialize a dictionary to store variables and their values

    def read(self, id):
        return self.variable[id]  # Return the value associated with the provided variable id

    def read_all(self):
        return self.variable  # Return the entire dictionary of variables and their values

    def write(self, variable, expression):
        variable_name = variable.value
        self.variable[variable_name] = expression  # Store the expression value in the dictionary
