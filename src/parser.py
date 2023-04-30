# this is the parser class for the compiler
# it's meant to parse the tokens created by the lexer class @(./lexer.py)
# and create an abstract syntax tree (AST) from them

from lexer import Token, TokenType
from asttree import (
    AstNode,
    OrAstNode,
    SeqAstNode,
    StarAstNode,
    PlusAstNode,
    QuestionMarkAstNode,
    LiteralCharacterAstNode,
    CharacterClassAstNode,
)
from typing import Tuple


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def parse(self) -> AstNode:
        return self.__parse(0)[0]

    def __parse(self, index: int) -> Tuple[AstNode, int]:
        return self.__parse_or(index)

    def __parse_or(self, index: int) -> Tuple[AstNode, int]:
        left, index = self.__parse_seq(index)
        rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            return (left, index)
        result = left
        while rem_tokens and self.tokens[index].token_type == TokenType.OR:
            index += 1
            right, index = self.__parse_seq(index)
            result = OrAstNode(result, right)
            rem_tokens = index < len(self.tokens)
        return (result, index)

    def __parse_seq(self, index: int) -> Tuple[AstNode, int]:
        left, index = self.__parse_counters(index)
        rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            return (left, index)
        result = left
        while (
            rem_tokens
            and self.tokens[index].token_type != TokenType.OR
            and self.tokens[index].token_type != TokenType.CLOSED_PARENTHESIS
        ):
            right, index = self.__parse_counters(index)
            result = SeqAstNode(result, right)
            rem_tokens = index < len(self.tokens)
        return (result, index)

    def __parse_counters(self, index: int) -> Tuple[AstNode, int]:
        left, index = self.__parse_base(index)
        rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            return (left, index)
        # if not rem_tokens:
        #     return (left, index)
        # if rem_tokens and self.tokens[index].token_type == TokenType.QUESTION_MARK:
        #     index += 1
        #     return (QuestionMarkAstNode(left), index)
        # if rem_tokens and self.tokens[index].token_type == TokenType.STAR:
        #     index += 1
        #     return (StarAstNode(left), index)
        # if rem_tokens and self.tokens[index].token_type == TokenType.PLUS:
        #     index += 1
        #     return (PlusAstNode(left), index)
        while rem_tokens and self.tokens[index].token_type in [TokenType.PLUS, TokenType.STAR, TokenType.QUESTION_MARK]:
            if rem_tokens and self.tokens[index].token_type == TokenType.QUESTION_MARK:
                index += 1
                left = QuestionMarkAstNode(left)
            elif rem_tokens and self.tokens[index].token_type == TokenType.STAR:
                index += 1
                left = StarAstNode(left)
            elif rem_tokens and self.tokens[index].token_type == TokenType.PLUS:
                index += 1
                left = PlusAstNode(left)
            rem_tokens = index < len(self.tokens)
        return (left, index)

    def __parse_square_bracket(self, index: int) -> Tuple[AstNode, int]:
        rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            raise Exception()
        chars = []
        end_range = False
        while rem_tokens and self.tokens[index].token_type != TokenType.CLOSED_SQUARE_BRACKET:
            if self.tokens[index].token_type == TokenType.DASH:
                end_range = True
            elif end_range:
                if len(chars) == 0:
                    raise Exception()
                start = chars.pop()
                end = self.tokens[index].value
                if start > end:
                    raise Exception()
                chars.append((start, end))
                end_range = False
            else:
                chars.append(self.tokens[index].value)
            index += 1
            rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            raise Exception()
        return (CharacterClassAstNode(set(chars)), index)

    def __parse_base(self, index: int) -> Tuple[AstNode, int]:
        rem_tokens = index < len(self.tokens)
        if not rem_tokens:
            raise Exception()
        current_token = self.tokens[index]
        index += 1
        if current_token.token_type == TokenType.LITERAL_CHARACTER:
            return (LiteralCharacterAstNode(current_token.value), index)
        if current_token.token_type == TokenType.OPEN_PARENTHESIS:
            left, index = self.__parse(index)
            rem_tokens = index < len(self.tokens)
            if not rem_tokens:
                raise Exception()
            if self.tokens[index].token_type != TokenType.CLOSED_PARENTHESIS:
                raise Exception()
            index += 1
            return (left, index)
        if current_token.token_type == TokenType.OPEN_SQUARE_BRACKET:
            left, index = self.__parse_square_bracket(index)
            rem_tokens = index < len(self.tokens)
            if not rem_tokens:
                raise Exception()
            if self.tokens[index].token_type != TokenType.CLOSED_SQUARE_BRACKET:
                raise Exception()
            index += 1
            return (left, index)
