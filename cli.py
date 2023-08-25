from language import Lexer, Parser
from compiler import Interpreter
from operation import Data

base = Data()

while True:
    output = input("Interpreter: ")

    value = Lexer(output)
    vals = value.tokenize()

    parser = Parser(vals)
    tree = parser.parse()

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()
    if result is not None:
        print(result)
