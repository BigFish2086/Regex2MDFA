# this file is to minimize the DFA into an MDFA

from typing import Dict, List, Tuple, Set
from nfa import State, EPSILON
from dfa import DFA, DFAClean, clean_dfa
from copy import deepcopy


class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


def minimize_dfa(cdfa: DFAClean) -> DFAClean:
    accepting_states = set(cdfa.accepting_states)
    rejecting_states = cdfa.all_states - accepting_states
    accepting_states = frozenset(accepting_states)
    rejecting_states = frozenset(rejecting_states)

    which_group = {}
    for state in cdfa.all_states:
        if state not in accepting_states:
            which_group[state] = rejecting_states
        else:
            which_group[state] = accepting_states

    mdfa_all_groups = {accepting_states, rejecting_states}
    still_splitting = True

    while still_splitting:
        still_splitting = False
        mdfa_all_groups_copy = deepcopy(mdfa_all_groups)
        for group in mdfa_all_groups:
            if len(group) > 1:
                possible_splits = {}
                for state in group:
                    state_transitions = Hashabledict()
                    for next_state, char in cdfa.transitions.get(state, []):
                        state_transitions[char] = which_group[next_state]

                    if state_transitions not in possible_splits:
                        possible_splits[state_transitions] = {state}
                    else:
                        possible_splits[state_transitions].add(state)

                if len(possible_splits) > 1:
                    still_splitting = True
                    mdfa_all_groups_copy.remove(group)
                    for new_group in possible_splits.values():
                        new_group = frozenset(new_group)
                        mdfa_all_groups_copy.add(new_group)
                        for state in new_group:
                            which_group[state] = new_group

                mdfa_all_groups = deepcopy(mdfa_all_groups_copy)

    mdfa_starting_state = which_group[cdfa.starting_state]

    mdfa_accepting_states = []
    for state in cdfa.accepting_states:
        mdfa_accepting_states.append(which_group[state])

    mdfa_transitions = {}
    for state, transitions in cdfa.transitions.items():
        mdfa_transitions[which_group[state]] = []
        for next_state, char in transitions:
            mdfa_transitions[which_group[state]].append((which_group[next_state], char))

    mdfa_all_states = set()
    for group in mdfa_all_groups:
        mdfa_all_states.add(frozenset(group))

    intermediate = DFA(mdfa_starting_state, mdfa_accepting_states, mdfa_transitions, mdfa_all_states)
    return clean_dfa(intermediate)
