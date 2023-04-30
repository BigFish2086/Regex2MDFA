import argparse
from lexer import Lexer
from parser import Parser
from nfa import ast_to_nfa, get_transition_table, get_starting_state, get_accepting_state
from dfa import build_powerset, clean_dfa
from mdfa import minimize_dfa
from logger import log_nfa, log_mdfa
from graph import visualize_nfa, visualize_dfa, visualize_clean_dfa, visualize_mdfa


def get_args():
    parser = argparse.ArgumentParser(description="A simple regex compiler that compiles a regex to a NFA")
    parser.add_argument(
        "regex",
        type=str,
        help="the regex to compile",
    )
    # make the verbose flag optional when given set it to true
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="expand ranges like [a-z] to [a, b, c, ..., z] not just [a-z] on one edge",
    )
    return parser.parse_args()


def run(input_regex: str, verbose: bool = False):
    lexer = Lexer(input_regex)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    print(tokens)
    print(ast)

    ast_to_nfa(ast, verbose=verbose)
    nfa = get_transition_table()

    starting_state = get_starting_state()
    accepting_state = get_accepting_state()
    log_nfa(nfa, starting_state, accepting_state)
    visualize_nfa(nfa, starting_state, accepting_state)

    dfa = build_powerset(starting_state, accepting_state, nfa)
    visualize_dfa(dfa)

    cdfa = clean_dfa(dfa)
    visualize_clean_dfa(cdfa)

    mdfa = minimize_dfa(cdfa)
    log_mdfa(mdfa)
    visualize_mdfa(mdfa, "MDFA")


def main():
    args = get_args()
    run(args.regex, args.verbose)


if __name__ == "__main__":
    main()


# regex = [
# "(AB)",
# "(A|B)",
# "([A-Z])",
# "(A+)",
# "(A*)",
# "(((AB)((A|B)*))(AB))",
# "((((AB)|[X-Z])+)([C-F]*))",
# "(((((ABE)|C)|((([A-C])S)*))+)((AB)C))",
# "((([a-e_])(([a-c0-3_])*))(([!?])?))",
# "(A(((B*)|(DA))*))((CG)|(D([DEF])))",
# "(ab",
# "(a([b-c))",
# "((a|b)|)",
# "(a{3,2})"
# ]
