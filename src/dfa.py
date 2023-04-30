# this file is used to generate the DFA from the NFA

from typing import Dict, List, Tuple, Set
from nfa import State, EPSILON
from copy import deepcopy


class DFA:
    def __init__(
        self,
        starting_state: frozenset[State],
        accepting_states: list[frozenset[State]],
        transitions: Dict[frozenset[State], Set[Tuple[frozenset[State], str]]],
        all_states: Set[frozenset[State]],
    ):
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.all_states = all_states


class DFAClean:
    def __init__(
        self,
        starting_state: State,
        accepting_states: list[State],
        transitions: Dict[State, Set[Tuple[State, str]]],
        all_states: Set[State],
    ):
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.all_states = all_states


def __get_epsilon_closure(nfa_start: State, nfa_transitions: Dict[State, List[Tuple[State, str]]]) -> Set[State]:
    """
    Returns the epsilon closure of the given NFA start state.

    Args:
        nfa_start: The start state of the NFA.
        nfa_transitions: The transitions of the NFA. it's in the form of:
        {from_state: [(to_state, transition_symbol|ε), ...], }

    Returns:
        The epsilon closure of the given NFA start state.
    """

    # A state R is in the epsilon closure of a state S if
    # 1- S is R
    # 2- R can be reached via an epsilon transition from any state in the epsilon closure of S
    epsilon_closure = set()
    epsilon_closure.add(nfa_start)
    still_adding = True
    while still_adding:
        still_adding = False
        for state in deepcopy(epsilon_closure):
            for next_state, char in nfa_transitions.get(state, []):
                if char == EPSILON and next_state not in epsilon_closure:
                    still_adding = True
                    epsilon_closure.add(next_state)
    return epsilon_closure


def build_powerset(
    nfa_start: State,
    nfa_accepting: State,
    nfa_transitions: Dict[State, List[Tuple[State, str]]],
) -> DFA:
    """
    Builds the powerset of the given NFA.

    Args:
        nfa_start: The start state of the NFA.
        nfa_accepting: The accepting state of the NFA.
        nfa_transitions: The transitions of the NFA. it's in the form of:
        {from_state: [(to_state, transition_symbol|ε), ...], }

    Returns:
        a DFA {starting_state, accepting_states, transitions, all_states}
    """

    dfa_start = __get_epsilon_closure(nfa_start, nfa_transitions)
    dfa_accept: List[frozenset[State]] = []
    dfa_states: Set[frozenset[State]] = set()
    dfa_transitions: Dict[frozenset[State], Set[Tuple[frozenset[State], str]]] = {}

    superstates_to_process: List[Set[State]] = [dfa_start]

    while superstates_to_process:
        superstate = superstates_to_process.pop()
        frozen_superstate = frozenset(superstate)
        dfa_states.add(frozen_superstate)
        if nfa_accepting in superstate:
            dfa_accept.append(frozen_superstate)

        superstate_transitions: Dict[str, Set[State]] = {}
        for state in superstate:
            for next_state, char in nfa_transitions.get(state, []):
                if char != EPSILON:
                    state_moving = __get_epsilon_closure(next_state, nfa_transitions)
                    if char in superstate_transitions:
                        superstate_transitions[char] = superstate_transitions[char].union(state_moving)
                    else:
                        superstate_transitions[char] = state_moving

        for char, next_superstate in superstate_transitions.items():
            frozen_next_superstate = frozenset(next_superstate)
            if frozen_superstate in dfa_transitions:
                dfa_transitions[frozen_superstate].add((frozen_next_superstate, char))
            else:
                dfa_transitions[frozen_superstate] = {(frozen_next_superstate, char)}
            if next_superstate not in dfa_states:
                superstates_to_process.append(next_superstate)

    return DFA(frozenset(dfa_start), dfa_accept, dfa_transitions, dfa_states)


def clean_dfa(dfa: DFA) -> DFAClean:
    """
    Cleans the given DFA i.e exchange the supersets with just a single state representing them.

    Args:
        dfa: The DFA to clean.

    Returns:
        A DFAClean {starting_state, accepting_states, transitions, all_states}
    """
    index = 0
    superstate_to_state: Dict[frozenset[State], State] = {}
    for superstate in dfa.all_states:
        superstate_to_state[superstate] = State(f"S{index}")
        index += 1
    clean_start = superstate_to_state[dfa.starting_state]
    clean_accepting = [superstate_to_state[superstate] for superstate in dfa.accepting_states]

    clean_transitions: Dict[State, Set[Tuple[State, str]]] = {}
    for superstate, transitions in dfa.transitions.items():
        for next_superstate, char in transitions:
            if superstate_to_state[superstate] in clean_transitions:
                clean_transitions[superstate_to_state[superstate]].add((superstate_to_state[next_superstate], char))
            else:
                clean_transitions[superstate_to_state[superstate]] = {(superstate_to_state[next_superstate], char)}

    clean_all_states = set(superstate_to_state.values())

    return DFAClean(clean_start, clean_accepting, clean_transitions, clean_all_states)
