# this file will be used to log down the nfa, dfa and mdfa
# into the json file with the desired format which is like this:
"""
{
    "startingState": "S0"
    "S0": {
        isTerminatingState: true,
        "0": "S0",
        "1": "S1"
    },
    "S1": {
        isTerminatingState: false,
        "0": "S2",
        "1": "S0"
    },
    "S2": {
        isTerminatingState: true,
        "0": "S1",
        "1": "S2"
    }
}
"""

import json
from typing import Dict, List, Tuple
from nfa import State, EPSILON
from dfa import DFAClean

__nfa_filename = "NFA.json"
__nfa_result: Dict[str, str | Dict[str, str | bool]] = {}

__mdfa_filename = "MDFA.json"
__mdfa_result: Dict[str, str | Dict[str, str | bool]] = {}


def __build_nfa_result(transition_table, accepting_state: State):
    accepted_labeled = False
    for state, transitions in transition_table.items():
        __nfa_result[state.label] = {}
        accepted_labeled = accepted_labeled or (state == accepting_state)
        for next_state, char in transitions:
            # if the char has been added before, then make it a list and append the next state
            if char in __nfa_result[state.label]:
                if isinstance(__nfa_result[state.label][char], list):
                    __nfa_result[state.label][char].append(next_state.label)
                else:
                    __nfa_result[state.label][char] = [__nfa_result[state.label][char], next_state.label]
            else:
                __nfa_result[state.label][char] = next_state.label
        __nfa_result[state.label]["isTerminatingState"] = state == accepting_state
    if not accepted_labeled:
        __nfa_result[accepting_state.label] = {"isTerminatingState": True}


def log_nfa(transition_table: Dict[State, List[Tuple[State, str]]], starting_state: State, accepting_state: State):
    __nfa_result.update({"startingState": starting_state.label})
    __build_nfa_result(transition_table, accepting_state)
    with open(__nfa_filename, "w") as f:
        json.dump(__nfa_result, f, ensure_ascii=False, indent=2)  # ensure utf-8 encoding


def __build_mdfa_result(mdfa: DFAClean):
    for state, transitions in mdfa.transitions.items():
        __mdfa_result[state.label] = {}
        for next_state, char in transitions:
            __mdfa_result[state.label][char] = next_state.label
        __mdfa_result[state.label]["isTerminatingState"] = state in mdfa.accepting_states


def log_mdfa(mdfa: DFAClean):
    __mdfa_result.update({"startingState": mdfa.starting_state.label})
    __build_mdfa_result(mdfa)
    with open(__mdfa_filename, "w") as f:
        json.dump(__mdfa_result, f, ensure_ascii=False, indent=2)
