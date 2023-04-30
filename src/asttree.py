# this class holds the AST nodes for the regex parser


class AstNode:
    pass


class OrAstNode(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} | {self.right})"

    def __repr__(self):
        return f"({self.left} | {self.right})"


class SeqAstNode(AstNode):
    def __init__(self, left: AstNode, right: AstNode):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.right})"

    def __repr__(self):
        return f"({self.left} {self.right})"


class StarAstNode(AstNode):
    def __init__(self, left: AstNode):
        self.left = left

    def __str__(self):
        return f"({self.left}*)"

    def __repr__(self):
        return f"({self.left}*)"


class PlusAstNode(AstNode):
    def __init__(self, left: AstNode):
        self.left = left

    def __str__(self):
        return f"({self.left}+)"

    def __repr__(self):
        return f"({self.left}+)"


class QuestionMarkAstNode(AstNode):
    def __init__(self, left: AstNode):
        self.left = left

    def __str__(self):
        return f"({self.left}?)"

    def __repr__(self):
        return f"({self.left}?)"


class LiteralCharacterAstNode(AstNode):
    def __init__(self, char: str):
        self.char = char

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char


class CharacterClassAstNode(AstNode):
    def __init__(self, char_class: set[str | tuple[str, str]]):
        self.char_class = char_class

    def __str__(self):
        return f"[{self.char_class}]"

    def __repr__(self):
        return f"[{self.char_class}]"
