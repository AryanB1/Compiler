# Import necessary classes from the respective modules
from language import Lexer, Parser
from compiler import Interpreter
from operation import Data

# Create an instance of the Data class to store variables and their values
base = Data()

# Continuous loop to take user input for interpretation
while True:
    # Prompt the user for input and store it in the 'output' variable
    output = input("Interpreter: ")

    # Tokenize the input using the Lexer class from the 'language' module
    value = Lexer(output)
    vals = value.tokenize()

    # Parse the tokenized values using the Parser class from the 'language' module
    parser = Parser(vals)
    tree = parser.parse()

    # Initialize an Interpreter instance with the parsed tree and the 'base' Data instance
    interpreter = Interpreter(tree, base)

    # Execute interpretation on the provided tree and data
    result = interpreter.interpret()

    # If the result of interpretation is not None, print the result
    if result is not None:
        print(result)
