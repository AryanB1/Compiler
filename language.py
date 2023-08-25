from operation import Integer, Float, Operation, Declaration, Variable, Boolean, Comparison, Reserved

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Initialize Parser with a list of tokens
        self.idx = 0  # Initialize token index to 0
        self.token = self.tokens[self.idx]  # Initialize current token

    def factor(self):
        # Determine the type of factor and return accordingly
        if self.token.type == "INT" or self.token.type == "FLT":
            return self.token
        elif self.token.value == "(":
            self.move()  # Move to the next token
            expression = self.boolean_expression()  # Recursively parse an expression
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            output = [operator, self.boolean_expression()]  # Create a "not" operation node
            return output

        elif self.token.type.startswith("VAR"):
            return self.token
        elif self.token.value == "+" or self.token.value == "-":
            operator = self.token
            self.move()
            operand = self.boolean_expression()  # Recursively parse an operand
            return [operator, operand]  # Create an operation node

    def term(self):
        left_node = self.factor()  # Get the left node
        self.move()

        while self.token.value == "*" or self.token.value == "/":
            operator = self.token
            self.move()
            right_node = self.factor()  # Get the right node
            self.move()

            left_node = [left_node, operator, right_node]  # Create a term operation node

        return left_node
    def if_statement(self):
        self.move()  # Move to the next token
        condition = self.boolean_expression()  # Parse the condition for the if statement

        if self.token.value == "do":
            self.move()
            action = self.statement()  # Parse the action inside the if statement

            return condition, action
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()  # Parse the action inside the if statement
            return condition, action

    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()  # Parse the initial if statement

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == "elif":
            if_statement = self.if_statement()  # Parse subsequent elif statements
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == "else":
            self.move()
            self.move()
            else_action = self.statement()  # Parse the else statement's action

            return [conditions, actions, else_action]

        return [conditions, actions]

    def while_statement(self):
        self.move()  # Move to the next token
        condition = self.boolean_expression()  # Parse the condition for the while statement

        if self.token.value == "do":
            self.move()
            action = self.statement()  # Parse the action inside the while loop
            return [condition, action]

        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()  # Parse the action inside the while loop
            return [condition, action]

    def comp_expression(self):
        left_node = self.expression()  # Parse the left node of the comparison expression
        while self.token.type == "COMP":
            operator = self.token
            self.move()
            right_node = self.expression()  # Parse the right node of the comparison expression
            left_node = [left_node, operator, right_node]  # Create a comparison node

        return left_node

    def boolean_expression(self):
        left_node = self.comp_expression()  # Parse the left node of the boolean expression

        while self.token.value == "and" or self.token.value == "or":
            operator = self.token
            self.move()
            right_node = self.comp_expression()  # Parse the right node of the boolean expression
            left_node = [left_node, operator, right_node]  # Create a boolean operation node

        return left_node

    def expression(self):
        left_node = self.term()  # Parse the left node of the arithmetic expression
        while self.token.value == "+" or self.token.value == "-":
            operator = self.token
            self.move()
            right_node = self.term()  # Parse the right node of the arithmetic expression
            left_node = [left_node, operator, right_node]  # Create an arithmetic operation node

        return left_node

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token  # Return the variable token

    def statement(self):
        if self.token.type == "DECL":
            # Variable assignment
            self.move()
            left_node = self.variable()  # Parse the left node (variable name)
            self.move()
            if self.token.value == "=":
                operation = self.token
                self.move()
                right_node = self.boolean_expression()  # Parse the right node (expression)
                return [left_node, operation, right_node]  # Create an assignment node

        elif self.token.type == "INT" or self.token.type == "FLT" or self.token.type == "OP" or self.token.value == "not":
            # Arithmetic or boolean expression
            return self.boolean_expression()  # Parse and return the expression

        elif self.token.value == "if":
            return [self.token, self.if_statements()]  # Parse if statements

        elif self.token.value == "while":
            return [self.token, self.while_statement()]  # Parse while loop statements

    def parse(self):
        return self.statement()  # Parse and return the statement
    def move(self):
        self.idx += 1  # Move to the next token
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]  # Update the current token
class Lexer:
    # while <expr> do <statement>
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-/*()="
    stopwords = [" "]
    declarations = ["make"]
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?="]
    specialCharacters = "><=?"
    reserved = ["if", "elif", "else", "do", "while"]

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                else:
                    self.token = Variable(word)

            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ""
                while self.char in Lexer.specialCharacters and self.idx < len(self.text):
                    comparisonOperator += self.char
                    self.move()

                self.token = Comparison(comparisonOperator)

            self.tokens.append(self.token)

        return self.tokens

    def extract_number(self):
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)

    def extract_word(self):
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()

        return word

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
