from backend.compiler.lexer.lexer import Lexer


code = """
let x = 10 + 20
let str = "hello"
"""

lexer = Lexer(code)

while True:

    token = lexer.next_token()

    print(token)

    if token.type == "EOF":
        break