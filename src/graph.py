# this file should be used to visualize the nfa, dfa and mdfa

import graphviz
from typing import Dict, List, Tuple
from nfa import State
from dfa import DFA, DFAClean


def visualize_nfa(
    transition_table: Dict[State, List[Tuple[State, str]]],
    starting_state: State,
    accepting_state: State,
    filename: str = "NFA",
):
    g = graphviz.Digraph("NFA", filename=filename, format="png")
    # make the graph horizontal
    g.attr(rankdir="LR")
    g.edge("", starting_state.label)  # add an arrow entering the starting state
    g.node("", shape="none")  # and remove the very first circle
    for state, transitions in transition_table.items():
        for next_state, char in transitions:
            g.edge(state.label, next_state.label, label=char)
    # add another oval for the accepting state
    g.node(accepting_state.label, peripheries="2")
    # add a title two lines under the graph
    g.attr(label=r"\n\nNFA", fontsize="20", labelloc="b")
    g.view()


def __frozenset_str(frozenset: frozenset[State]) -> str:
    """
    Returns the name of the given frozenset like in set.__str__
    """
    return "{" + ", ".join([state.label for state in frozenset]) + "}"


def visualize_dfa(dfa: DFA, filename: str = "DFA"):
    g = graphviz.Digraph("DFA", filename=filename, format="png")
    g.attr(rankdir="LR")
    g.edge("", __frozenset_str(dfa.starting_state))
    g.node("", shape="none")
    for state, transitions in dfa.transitions.items():
        x = __frozenset_str(state)
        for next_state, char in transitions:
            y = __frozenset_str(next_state)
            g.edge(x, y, label=char)
    for accepting_state in dfa.accepting_states:
        g.node(__frozenset_str(accepting_state), peripheries="2")
    g.attr(label=r"\n\nDFA", fontsize="20", labelloc="b")
    g.view()


def visualize_clean_dfa(clean_dfa: DFAClean, filename: str = "DFAClean"):
    g = graphviz.Digraph("DFAClean", filename=filename, format="png")
    g.attr(rankdir="LR")
    g.edge("", clean_dfa.starting_state.label)
    g.node("", shape="none")
    for state, transitions in clean_dfa.transitions.items():
        for next_state, char in transitions:
            g.edge(state.label, next_state.label, label=char)
    for accepting_state in clean_dfa.accepting_states:
        g.node(accepting_state.label, peripheries="2")
    g.attr(label=r"\n\nDFA Clean", fontsize="20", labelloc="b")
    g.view()


def visualize_mdfa(mdfa: DFAClean, filename: str = "MDFA"):
    g = graphviz.Digraph("MDFA", filename=filename, format="png")
    g.attr(rankdir="LR")
    g.edge("", mdfa.starting_state.label)
    g.node("", shape="none")
    for state, transitions in mdfa.transitions.items():
        for next_state, char in transitions:
            g.edge(state.label, next_state.label, label=char)
    for accepting_state in mdfa.accepting_states:
        g.node(accepting_state.label, peripheries="2")
    g.attr(label=r"\n\nMinimized DFA", fontsize="20", labelloc="b")
    g.view()
