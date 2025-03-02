class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        for dest_states in self.transitions.values():
            if len(dest_states) > 1:
                return False
        return True

    def to_regular_grammar(self):
        grammar = {state: [] for state in self.states}
        for state in self.final_states:
            grammar[state].append("ε")
        for (state, symbol), dest_states in self.transitions.items():
            for dest in dest_states:
                production = f"{symbol}{dest}"
                grammar[state].append(production)
        return RegularGrammar(grammar)

    def ndfa_to_dfa(self):
        initial = frozenset([self.start_state])
        dfa_states = {initial}
        dfa_transitions = {}
        dfa_final_states = set()
        if any(state in self.final_states for state in initial):
            dfa_final_states.add(initial)
        unmarked_states = [initial]
        while unmarked_states:
            current = unmarked_states.pop()
            for symbol in self.alphabet:
                new_state = set()
                for state in current:
                    new_state |= self.transitions.get((state, symbol), set())
                new_state = frozenset(new_state)
                if not new_state:
                    continue
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unmarked_states.append(new_state)
                    if any(state in self.final_states for state in new_state):
                        dfa_final_states.add(new_state)
                dfa_transitions[(current, symbol)] = new_state
        return DFA(dfa_states, self.alphabet, dfa_transitions, initial, dfa_final_states)


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def __str__(self):
        def format_state(state):
            return "{" + ", ".join(sorted(state)) + "}" if state else "{}"

        lines = [
            "Converted DFA:",
            f"  States: {[format_state(s) for s in self.states]}",
            f"  Alphabet: {self.alphabet}",
            f"  Start State: {format_state(self.start_state)}",
            f"  Final States: {[format_state(s) for s in self.final_states]}",
            "  Transitions:"
        ]
        for (state, symbol), dest in self.transitions.items():
            lines.append(f"    {format_state(state)} --{symbol}--> {format_state(dest)}")
        return "\n".join(lines)


class RegularGrammar:
    def __init__(self, productions):
        self.productions = productions

    def classify(self):
        return "Regular Grammar (Type-3)"

    def __str__(self):
        lines = ["Regular Grammar Productions:"]
        for non_terminal, prods in self.productions.items():
            for prod in prods:
                lines.append(f"  {non_terminal} -> {prod}")
        return "\n".join(lines)


def main():
    states = {"q0", "q1", "q2", "q3", "q4"}
    alphabet = {"a", "b", "c"}
    transitions = {
        ("q0", "a"): {"q1"},
        ("q1", "b"): {"q2", "q3"},
        ("q2", "c"): {"q3"},
        ("q3", "a"): {"q3"},
        ("q3", "b"): {"q4"}
    }
    start_state = "q0"
    final_states = {"q4"}

    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
    print("Automaton Type:", "DFA" if fa.is_deterministic() else "NDFA")

    dfa = fa.ndfa_to_dfa()
    print("\n" + str(dfa))

    grammar = fa.to_regular_grammar()
    print("\n" + str(grammar))
    print("\nGrammar Classification:", grammar.classify())


if __name__ == '__main__':
    main()
