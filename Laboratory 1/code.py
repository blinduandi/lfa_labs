import random

class Grammar:
    def __init__(self):
        self.non_terminals = ['S', 'R', 'L']
        self.terminals = ['a', 'b', 'c', 'd', 'e', 'f']
        self.start_symbol = 'S'
        self.productions = {
            'S': [('a', 'S'),
                  ('b', 'S'),
                  ('c', 'R'),
                  ('d', 'L')],
            'R': [('d', 'L'),
                  ('e', None)],
            'L': [('f', 'L'),
                  ('e', 'L'),
                  ('d', None)]
        }

    def generate_string(self, allow_invalid=False, invalid_prob=0.3):
        current = self.start_symbol
        result = ""
        while current is not None:
            productions = self.productions.get(current, [])
            if not productions:
                break
            prod = random.choice(productions)
            terminal, next_nt = prod
            result += terminal
            current = next_nt
        if allow_invalid and random.random() < invalid_prob:
            result += random.choice(self.terminals)
        return result

    def to_finite_automaton(self):
        states = set(self.non_terminals)
        final_state = 'F'
        states.add(final_state)
        transitions = {state: {} for state in states}
        for non_terminal, prods in self.productions.items():
            for symbol, next_nt in prods:
                if next_nt is None:
                    transitions[non_terminal][symbol] = final_state
                else:
                    transitions[non_terminal][symbol] = next_nt
        return FiniteAutomaton(
            states=states,
            alphabet=self.terminals,
            transitions=transitions,
            start_state=self.start_symbol,
            final_states={final_state}
        )

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if symbol not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][symbol]
        return current_state in self.final_states

if __name__ == "__main__":
    grammar = Grammar()
    print("Generated valid strings:")
    for _ in range(5):
        generated = grammar.generate_string()
        print(f"  {generated}")

    print("\nGenerated strings (with potential invalidity):")
    for _ in range(5):
        generated = grammar.generate_string(allow_invalid=True, invalid_prob=0.5)
        print(f"  {generated}")

    fa = grammar.to_finite_automaton()

    print("\nFinite Automaton Testing (with potential invalid strings):")
    test_strings = [grammar.generate_string(allow_invalid=True, invalid_prob=0.5) for _ in range(5)]
    for s in test_strings:
        accepted = fa.string_belongs_to_language(s)
        print(f"  String: {s}  Accepted: {accepted}")
