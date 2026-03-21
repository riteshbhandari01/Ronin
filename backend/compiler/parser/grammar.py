
from ..lexer.lexer import Lexer

class Grammar:

    def __init__(self, code):
        self.lexer = Lexer(code)
        self.currentToken = self.lexer.next_token()

    # 🔹 match function (strict + safe)
    def match(self, expected):
        # debug
        print(f"Token -> {self.currentToken.type}:{self.currentToken.value}")

        # keyword check
        if self.currentToken.type == "keyword" and self.currentToken.value == expected:
            self.currentToken = self.lexer.next_token()

        # symbol check ({ } etc.)
        elif self.currentToken.type == "symbol" and self.currentToken.value == expected:
            self.currentToken = self.lexer.next_token()

        # type check (IDENTIFIER, number etc.)
        elif self.currentToken.type == expected:
            self.currentToken = self.lexer.next_token()

        else:
            raise Exception(
                f"Syntax Error: expected {expected}, got {self.currentToken.value} at line {self.currentToken.line}"
            )

    # =========================
    # Expression Handling
    # expression → term (+|-) term
    # term → factor (*|/) factor
    # factor → number | identifier
    # =========================

    def factor(self):
        if self.currentToken.type == "number":
            self.match("number")

        elif self.currentToken.type == "IDENTIFIER":
            self.match("IDENTIFIER")

        else:
            raise Exception(f"Invalid factor at line {self.currentToken.line}")

    def term(self):
        self.factor()

        while self.currentToken.value in ["*", "/"]:
            self.match("arop")
            self.factor()

    def expression(self):
        self.term()

        while self.currentToken.value in ["+", "-"]:
            self.match("arop")
            self.term()

    # =========================
    # Conditions
    # =========================

    def condition(self):
        self.expression()
        self.match("relop")   # >, <, == etc.
        self.expression()

    # =========================
    # Statements
    # =========================

    def var_decl(self):
        self.match("let")
        self.match("IDENTIFIER")
        self.match("assig")
        self.expression()

    def if_condition(self):
        self.match("if")
        self.condition()
        self.match("{")
        self.body()
        self.match("}")

    def while_loop(self):
        self.match("while")
        self.condition()
        self.match("{")
        self.body()
        self.match("}")

    def stmt(self):
        if self.currentToken.type == "keyword" and self.currentToken.value == "let":
            self.var_decl()

        elif self.currentToken.type == "keyword" and self.currentToken.value == "if":
            self.if_condition()

        elif self.currentToken.type == "keyword" and self.currentToken.value == "while":
            self.while_loop()

        else:
            raise Exception(f"Unknown statement at line {self.currentToken.line}")

    def body(self):
        while not (self.currentToken.type == "symbol" and self.currentToken.value == "}"):
            if self.currentToken.type == "EOF":
                raise Exception("Missing closing '}'")
            self.stmt()

    def stmtList(self):
        while self.currentToken.type != "EOF":
            self.stmt()

    def start(self):
        self.stmtList()
        print("✅ Parsing completed successfully")


# =========================
# TEST CODE
# =========================

code = """
if 10 > 5 {
    let a = 10 + 20 * 3
}
"""

if __name__ == "__main__":
    parser = Grammar(code)
    parser.start()