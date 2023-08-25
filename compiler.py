from operation import Integer, Float, Reserved


class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def read_INT(self, value):
        return int(value)

    def read_FLT(self, value):
        return float(value)

    def read_VAR(self, id):
        variable = self.data.read(id)
        variable_type = variable.type

        return getattr(self, f"read_{variable_type}")(variable.value)

    def compute_bin(self, l, op, r):
        l_type = "VAR" if str(l.type).startswith("VAR") else str(l.type)
        r_type = "VAR" if str(r.type).startswith("VAR") else str(r.type)
        if op.value == "=":
            l.type = f"VAR({r_type})"
            self.data.write(l, r)
            return self.data.read_all()

        l = getattr(self, f"read_{l_type}")(l.value)
        r = getattr(self, f"read_{r_type}")(r.value)

        if op.value == "+":
            output = l + r
        elif op.value == "-":
            output = l - r
        elif op.value == "*":
            output = l * r
        elif op.value == "/":
            output = l / r
        elif op.value == ">":
            output = 1 if l > r else 0
        elif op.value == ">=":
            output = 1 if l >= r else 0
        elif op.value == "<":
            output = 1 if l < r else 0
        elif op.value == "<=":
            output = 1 if l <= r else 0
        elif op.value == "?=":
            output = 1 if l == r else 0
        elif op.value == "and":
            output = 1 if l and r else 0
        elif op.value == "or":
            output = 1 if l or r else 0

        return Integer(output) if (l_type == "INT" and r_type == "INT") else Float(output)

    def compute_unary(self, operator, operand):
        operand_type = "VAR" if str(operand.type).startswith("VAR") else str(operand.type)

        operand = getattr(self, f"read_{operand_type}")(operand.value)

        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output = 1 if not operand else 0

        return Integer(output) if (operand_type == "INT") else Float(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].value == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.value == 1:
                            return self.interpret(tree[1][1][idx])

                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    else:
                        return
                elif tree[0].value == "while":
                    condition = self.interpret(tree[1][0])
                    while condition.value == 1:
                        print(self.interpret(tree[1][1]))
                        condition = self.interpret(tree[1][0])
                    return
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)
        elif not isinstance(tree, list):
            return tree

        else:
            l_node = tree[0]
            if isinstance(l_node, list):
                l_node = self.interpret(l_node)

            r_node = tree[2]
            if isinstance(r_node, list):
                r_node = self.interpret(r_node)

            operator = tree[1]
            return self.compute_bin(l_node, operator, r_node)
