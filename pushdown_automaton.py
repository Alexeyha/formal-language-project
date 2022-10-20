import sys
from functools import reduce
import pathlib
import ply.yacc as yacc

from parse import *

from typing import Set, List, Union
from dataclasses import dataclass


@dataclass
class Left:
    state: str
    input_symbol: Terminal
    stack_symbol: NonTerminal

    def output(self):
        result = "\t\tLeft: {\n\t\t\tState: "
        result += self.state
        result += '\n\t\t\tInput symbol: '
        result += self.input_symbol.output()
        result += '\n\t\t\tStack symbol: '
        result += self.stack_symbol.output()
        result += '\n\t\t}\n'
        return result


@dataclass
class Right:
    state: str
    stack_sequence: Sequence

    def output(self):
        result = "\t\tRight: {\n\t\t\tState: "
        result += self.state
        result += '\n\t\t\tStack sequence: '
        result += self.stack_sequence.output()
        result += '\n\t\t}\n'
        return result


@dataclass
class Rule:
    left: Left
    right: Right

    def output(self):
        result = "\tRule: {\n"
        result += self.left.output()
        result += self.right.output()
        result += '\t}\n'
        return result


@dataclass
class PushdownAutomaton:
    states: List[str]
    input_alphabet: Set[str]
    stack_alphabet: Set[str]
    start_state: str
    start_stack_element: str
    rules: List[Rule]

    def output(self):
        result = 'States: '
        for state in self.states:
            result += state + ' '
        result += '\n'

        result += 'Input alphabet: '
        for alpha in self.input_alphabet:
            result += alpha + ', '
        result = result.removesuffix(', ')
        result += '\n'

        result += 'Stack alphabet: '
        for alpha in self.stack_alphabet:
            result += alpha + ', '
        result = result.removesuffix(', ')
        result += '\n'

        result += 'Start state: '
        result += self.start_state
        result += '\n'

        result += 'Start stack element: '
        result += self.start_stack_element
        result += '\n'

        result += 'Rules: {\n'
        for rule in self.rules:
            result += rule.output()
        result += '}'
        return result


def build_automaton(gram: Grammar) -> PushdownAutomaton:
    states = ["q0"]
    rules = []
    input_alphabet = gram.terminals
    stack_alphabet = gram.nonterminals
    start_state = states[0]
    start_stack_element = gram.start
    for bind in gram.binds:
        for sequence in bind.description.sequences:
            left = Left(states[0], sequence.singles[0], bind.source)
            if len(sequence.singles) == 1:
                right = Right(states[0], Sequence([Empty()]))
            else:
                right = Right(states[0], Sequence(sequence.singles[1::]))

            rules.append(Rule(left, right))

    return PushdownAutomaton(states, input_alphabet, stack_alphabet, start_state, start_stack_element, rules)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <run_file> <input_file>")
        return

    input_file = str(sys.argv[1])
    output_file = input_file + ".out"

    with open(input_file, "r") as f_input, open(output_file, "w") as f_output:
        parser = yacc.yacc(start="grammars")
        grammars = parser.parse("".join(f_input.readlines()))
        pushdown_automaton = build_automaton(grammars)
        print(pushdown_automaton.output(), file=f_output)


if __name__ == "__main__":
    main()
