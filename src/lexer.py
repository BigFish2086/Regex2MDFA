# this is the lexer class for the compiler
# it is used to tokenize the input file

from enum import Enum, auto


# | * + ? ( ) [ ] - are the meta characters
class TokenType(Enum):
    OR = auto()
    STAR = auto()
    PLUS = auto()
    DASH = auto()
    LITERAL_CHARACTER = auto()
    QUESTION_MARK = auto()
    OPEN_PARENTHESIS = auto()
    CLOSED_PARENTHESIS = auto()
    OPEN_SQUARE_BRACKET = auto()
    CLOSED_SQUARE_BRACKET = auto()


class Token:
    def __init__(self, token_type: TokenType, value: str | None):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"<{self.token_type}, {self.value}>"

    def __repr__(self):
        return f"<{self.token_type}, {self.value}>"


class Lexer:
    Escape_Character = "/"
    Meta_Characters_Map = {
        "|": TokenType.OR,
        "*": TokenType.STAR,
        "+": TokenType.PLUS,
        "?": TokenType.QUESTION_MARK,
        "(": TokenType.OPEN_PARENTHESIS,
        ")": TokenType.CLOSED_PARENTHESIS,
        "[": TokenType.OPEN_SQUARE_BRACKET,
        "]": TokenType.CLOSED_SQUARE_BRACKET,
        "-": TokenType.DASH,
    }

    def __init__(self, input_regex: str):
        self.input_regex = input_regex
        self.tokens = []

    def tokenize(self) -> list[Token]:
        prev_char = None
        for char in self.input_regex:
            if char == Lexer.Escape_Character:
                prev_char = char
                continue
            if char in Lexer.Meta_Characters_Map and prev_char != Lexer.Escape_Character:
                self.tokens.append(Token(Lexer.Meta_Characters_Map[char], char))
            else:
                self.tokens.append(Token(TokenType.LITERAL_CHARACTER, char))
            prev_char = char
        return self.tokens


# Note: Lexer completely ignores escape character,
# so whatever character you choose for #them, it’s one you can’t match literally
# (and you can easily modify it to allow escaping #the escapes themselves)
