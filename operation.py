class Operations:
    def __init__(self, type, var):
        self.type = type
        self.var = var

    def __repr__(self):
        return str(self.var)


class Integer(Operations):
    def __init__(self, var):
        super().__init__("INT", var)


class Float(Operations):
    def __init__(self, var):
        super().__init__("FLT", var)


class Operation(Operations):
    def __init__(self, var):
        super().__init__("OP", var)


class Declaration(Operations):
    def __init__(self, var):
        super().__init__("DECL", var)


class Variable(Operations):
    def __init__(self, var):
        super().__init__("VAR(?)", var)  # Variable name, VAR, data type
        # make a = 5 # VAR(?)


class Boolean(Operations):
    def __init__(self, var):
        super().__init__("BOOL", var)


class Comparison(Operations):
    def __init__(self, var):
        super().__init__("COMP", var)


class Reserved(Operations):
    def __init__(self, var):
        super().__init__("RSV", var)


class Data:
    def __init__(self):
        self.variable = {}

    def read(self, id):
        return self.variable[id]

    def read_all(self):
        return self.variable

    def write(self, variable, expression):
        variable_name = variable.value
        self.variable[variable_name] = expression

