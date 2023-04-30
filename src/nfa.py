# this file takes an AST (parser.parser()) and compiles it to a NFA
# using Thompson's construction algorithm

# ast file has the following classes:
#   - AstNode (abstract class)
#   - OrAstNode, SeqAstNode, StarAstNode, PlusAstNode,
#   - QuestionMarkAstNode, LiteralCharacterAstNode, CharacterClassAstNode

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
from enum import Enum
from typing import Dict, List, Set, Tuple


class State:
    def __init__(self, label: str, accept: bool = False):
        self.label = label
        self.accept = accept

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label

    def __eq__(self, other):
        if isinstance(other, State):
            return self.label == other.label
        return False

    def __lt__(self, other):
        if isinstance(other, State):
            return self.label < other.label
        return False

    def __hash__(self):
        return hash(self.label)


class ThompsonNFA:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end


EPSILON = "ε"


# transition table will be like this:
# {from_state: [(to_state, char)]}
# where from_state is the state that the transition is coming from
# and to_state is the state that the transition is going to
# and char is the character that the transition is on the edge & epsilons
__transition_table: Dict[State, List[Tuple[State, str]]] = {}

# to store the initial and terminal states of the NFA
__starting_state, __accepting_state = State(None), State(None)

# set the verbosity level of the NFA
# i.e whether to expand ranges like [a-z] to [a, b, c, ..., z] or not
__verbose = False


def get_transition_table() -> Dict[State, List[Tuple[State, str]]]:
    return __transition_table


def get_starting_state() -> State:
    global __starting_state
    return __starting_state


def get_accepting_state() -> State:
    global __accepting_state
    return __accepting_state


def ast_to_nfa(root: AstNode, verbose: bool = False) -> None:
    global __verbose
    __verbose = verbose
    _, _ = __ast_to_nfa(root=root, index=0)
    # __transition_table[nfa.start] = [(nfa.end, EPSILON)]


def __add_transition(from_state: State, to_state: State, char: str) -> None:
    global __transition_table
    if from_state not in __transition_table:
        __transition_table[from_state] = []
    # print(f"adding transition from {from_state} to {to_state} on {char}")
    __transition_table[from_state].append((to_state, char))


def __update_start_finish(start: State, end: State) -> None:
    global __starting_state, __accepting_state
    __starting_state = start
    __accepting_state = end


def __ast_to_nfa(root: AstNode, index: int = 0) -> Tuple[ThompsonNFA, int]:
    global __verbose
    if root is None:
        start = State(f"S{index}")
        end = State(f"S{index + 1}")
        __update_start_finish(start, end)
        # __add_transition(start, end, EPSILON)
        return ThompsonNFA(start, end), index + 2
    if isinstance(root, LiteralCharacterAstNode):
        return __literal_character_ast_to_nfa(root.char, index)
    if isinstance(root, OrAstNode):
        return __or_ast_to_nfa(root, index)
    if isinstance(root, SeqAstNode):
        return __seq_ast_to_nfa(root, index)
    if isinstance(root, StarAstNode):
        return __star_ast_to_nfa(root, index)
    if isinstance(root, PlusAstNode):
        return __plus_ast_to_nfa(root, index)
    if isinstance(root, QuestionMarkAstNode):
        return __question_mark_ast_to_nfa(root, index)
    if isinstance(root, CharacterClassAstNode):
        if __verbose:
            return __character_class_ast_to_nfa_verbose(root, index)
        else:
            return __character_class_ast_to_nfa(root, index)


def __literal_character_ast_to_nfa(root_char: str, index: int) -> Tuple[ThompsonNFA, int]:
    start = State(f"S{index}")
    end = State(f"S{index + 1}")
    __add_transition(start, end, root_char)
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 2


def __or_ast_to_nfa(root: OrAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
          -e-> S2 -a-> S3 -e->
         //                   \\
     -> S0                     -> S6
         \\                   //
          -e-> S4 -b-> S5 -e->
    """
    start = State(f"S{index}")  # S0
    left_nfa, index = __ast_to_nfa(root.left, index + 1)
    right_nfa, index = __ast_to_nfa(root.right, index + 1)
    end = State(f"S{index}")  # S6
    __add_transition(start, left_nfa.start, EPSILON)  # S0 -e-> S2
    __add_transition(start, right_nfa.start, EPSILON)  # S0 -e-> S4
    __add_transition(left_nfa.end, end, EPSILON)  # S3 -e-> S6
    __add_transition(right_nfa.end, end, EPSILON)  # S5 -e-> S6
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 1


def __seq_ast_to_nfa(root: SeqAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
    -> S0 -a-> S1 -e-> S2 -b-> S3
    """
    start = State(f"S{index}")  # S0
    left_nfa, index = __ast_to_nfa(root.left, index + 1)
    right_nfa, index = __ast_to_nfa(root.right, index + 1)
    __add_transition(start, left_nfa.start, EPSILON)  # S0 -e-> S1
    __add_transition(left_nfa.end, right_nfa.start, EPSILON)  # S2 -e-> S3
    __update_start_finish(start, right_nfa.end)
    return ThompsonNFA(start, right_nfa.end), index + 1


def __star_ast_to_nfa(root: StarAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
        v------e-------|
    -> S0 -e-> S1 -a-> S2 -e-> S3
        ^---------e------------|
    """
    start = State(f"S{index}")  # S0
    nfa, index = __ast_to_nfa(root.left, index + 1)
    end = State(f"S{index}")  # S3
    __add_transition(start, end, EPSILON)  # S0 -e-> S3
    __add_transition(start, nfa.start, EPSILON)  # S0 -e-> S1
    __add_transition(nfa.end, end, EPSILON)  # S2 -e-> S3
    __add_transition(nfa.end, nfa.start, EPSILON)  # S2 -e-> S1
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 1


def __plus_ast_to_nfa(root: PlusAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
        v------e-------|
    -> S0 -e-> S1 -a-> S2 -e-> S3
    """
    start = State(f"S{index}")  # S0
    nfa, index = __ast_to_nfa(root.left, index + 1)
    end = State(f"S{index}")  # S3
    __add_transition(start, nfa.start, EPSILON)  # S0 -e-> S1
    __add_transition(nfa.end, end, EPSILON)  # S2 -e-> S3
    __add_transition(nfa.end, nfa.start, EPSILON)  # S2 -e-> S1
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 1


def __question_mark_ast_to_nfa(root: QuestionMarkAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
        |------e-------v
    -> S0 -e-> S1 -a-> S2
                |--e---^
    """
    start = State(f"S{index}")  # S0
    nfa, index = __ast_to_nfa(root.left, index + 1)
    end = State(f"S{index}")  # S2
    __add_transition(start, end, EPSILON)  # S0 -e-> S2
    __add_transition(start, nfa.start, EPSILON)  # S0 -e-> S1
    __add_transition(nfa.end, end, EPSILON)  # S2 -e-> S2
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 1


def __character_class_ast_to_nfa(root: CharacterClassAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
    this time root it has a set[str | Tuple[str, str]] so in
    1. just a char: it's just a literal char
    2. a range: it's a range of chars like [a-z] => "a-z" for simplicity
        2.a it could be written as [abc...z], later maybe !
        2.b in case of reversed range => the parser will throw an error
    then consider all of the result as ored literals
    """
    start = State(f"S{index}")  # S0
    nfas = []
    for char in root.char_class:
        if isinstance(char, str):
            value = char
        else:
            value = f"{char[0]}-{char[1]}"
        nfa, index = __literal_character_ast_to_nfa(value, index + 1)
        nfas.append(nfa)

    # or each 2 nfas together
    while len(nfas) > 1:
        nfa1 = nfas.pop()
        nfa2 = nfas.pop()
        semi_start = State(f"S{index + 1}")  # S0
        semi_end = State(f"S{index + 2}")  # S1
        __add_transition(semi_start, nfa1.start, EPSILON)  # S0 -e-> S1
        __add_transition(semi_start, nfa2.start, EPSILON)  # S0 -e-> S2
        __add_transition(nfa1.end, semi_end, EPSILON)  # S3 -e-> S4
        __add_transition(nfa2.end, semi_end, EPSILON)  # S5 -e-> S4
        nfas.append(ThompsonNFA(semi_start, semi_end))
        index += 2

    end = State(f"S{index + 1}")  # S1
    __add_transition(nfas[0].end, end, EPSILON)  # S3 -e-> S4
    __add_transition(start, nfas[0].start, EPSILON)  # S0 -e-> S1
    __update_start_finish(start, end)
    return ThompsonNFA(start, end), index + 2


# def __character_class_ast_to_nfa_verbose(root: CharacterClassAstNode, index: int) -> Tuple[ThompsonNFA, int]:
# """
#                     -e-> S2 -a-> S3 -e->
#                   //                    \\
#               -> S0                     S6 ->
#             //    \\                    //   \\
#            //      -e-> S4 -b-> S5 -e-->      \\
#        -> S0                                   S7 ->
#            \\                                 //
#             \\                               //
#              ---e----> S4 -b-> S5 -----e----->
# """
#     def build_or_ast_from_set(chars: Set[str]) -> AstNode:
#         if len(chars) == 1:
#             return LiteralCharacterAstNode(chars.pop())
#         else:
#             char = chars.pop()
#             return OrAstNode(LiteralCharacterAstNode(char), build_or_ast_from_set(chars))
#     all_chars = set()
#     for char in root.char_class:
#         if isinstance(char, str):
#             all_chars.add(char)
#         else:
#             for c in range(ord(char[0]), ord(char[1]) + 1):
#                 all_chars.add(chr(c))
#     return __ast_to_nfa(build_or_ast_from_set(all_chars), index)


def __character_class_ast_to_nfa_verbose(root: CharacterClassAstNode, index: int) -> Tuple[ThompsonNFA, int]:
    """
          ---------a-------->
         //                 \\
     -> S0 ---------b-------> S1
         \\                 //
          ---------c-------->
    """
    start = State(f"S{index}")  # S0
    index += 1
    end = State(f"S{index}")

    all_chars = set()
    for char in root.char_class:
        if isinstance(char, str):
            all_chars.add(char)
        else:
            for c in range(ord(char[0]), ord(char[1]) + 1):
                all_chars.add(chr(c))

    for char in all_chars:
        __add_transition(start, end, char)

    __update_start_finish(start, end)

    return ThompsonNFA(start, end), index + 1
