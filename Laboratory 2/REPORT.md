# Determinism in Finite Automata: NDFA to DFA Conversion and Regular Grammar Derivation

**Course:** Formal Languages & Finite Automata  
**Author:** Cretu Dumitru  
**Acknowledgments:** Kudos to Vasile Drumea and Irina Cojuhari\
**Student:** Blindu Andi FAF-233

---

## 1. Introduction

Finite automata are abstract machines that play a key role in the study of formal languages and computation. They model processes with a finite number of states. In this project, we focus on:

- Verifying whether a given automaton is deterministic or non-deterministic.
- Converting a non-deterministic finite automaton (NDFA) to a deterministic finite automaton (DFA) using the subset construction algorithm.
- Deriving the equivalent regular grammar (right-linear grammar) from the finite automaton, thereby confirming its position in the Chomsky hierarchy (Type 3).

---

## 2. Problem Statement

For **Variant 2**, the automaton is defined as follows:

- **States:** \( Q = \{q0, q1, q2, q3, q4\} \)
- **Alphabet:** \( Σ = \{a, b, c\} \)
- **Final State:** \( F = \{q4\} \)
- **Transitions:**
  - \( Δ(q0, a) = \{q1\} \)
  - \( Δ(q1, b) = \{q2, q3\} \) *(non-deterministic: two possible transitions on 'b')*
  - \( Δ(q2, c) = \{q3\} \)
  - \( Δ(q3, a) = \{q3\} \)
  - \( Δ(q3, b) = \{q4\} \)

The objectives are to verify the automaton’s determinism, convert the NDFA to a DFA, and derive its corresponding regular grammar.

---

## 3. Theoretical Background

### 3.1 Determinism vs. Non-Determinism

- **Deterministic Finite Automata (DFA):**  
  Every state has exactly one transition for each input symbol, ensuring a unique computation path.

- **Non-Deterministic Finite Automata (NDFA):**  
  States may have multiple transitions for a given symbol, leading to several possible computation paths. It is established that every NDFA can be converted into an equivalent DFA.

### 3.2 Subset Construction Algorithm

The NDFA-to-DFA conversion uses the subset construction algorithm, which involves:

1. **Initial State:**  
   The DFA's start state is the set containing the NDFA’s start state (e.g., \(\{q0\}\)).
   
2. **Transitions:**  
   For each DFA state (a set of NDFA states) and for each symbol, compute the union of transitions from the NDFA states. Each resulting union represents a new DFA state.
   
3. **Final States:**  
   Any DFA state that contains at least one NDFA final state is marked as accepting.

### 3.3 Conversion to Regular Grammar

A finite automaton can be converted into a regular (right-linear) grammar by following these rules:

- **Production Rules:**  
  For each transition \( Δ(q_i, a) = q_j \), add a production \( A_i \rightarrow aA_j \), where \( A_i \) and \( A_j \) correspond to states \( q_i \) and \( q_j \), respectively.
  
- **Epsilon Productions:**  
  For every final state \( q_f \), include an epsilon production \( A_f \rightarrow \epsilon \) to allow termination of derivations.

---

## 4. Implementation

The project is implemented in Python. The implementation consists of two main parts:

- **FiniteAutomaton Class:**  
  This part defines the NDFA, includes a method to check for determinism, implements the subset construction algorithm for NDFA-to-DFA conversion, and contains a method to derive the regular grammar.

- **DFA Class:**  
  Represents the resulting deterministic finite automaton and provides methods for formatted output.

### 4.1 Code


```python

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


```

---

## 5. Testing and Results

When executed, the program performs the following:

- **Determinism Check:**  
  It verifies that the original automaton is non-deterministic (e.g., state `q1` has two transitions on symbol `b`).

- **NDFA to DFA Conversion:**  
  The subset construction algorithm converts the NDFA to a DFA. The DFA states are represented as sets of NDFA states, and the transitions are listed accordingly.

- **Regular Grammar Derivation:**  
  The automaton is converted into a right-linear grammar with production rules derived from the transitions, including epsilon productions for final states.

The results confirm that the conversion processes work correctly and that the derived regular grammar accurately represents the language of the original automaton.

---

## 6. Conclusion

This project demonstrates the conversion of a non-deterministic finite automaton into a deterministic one using the subset construction algorithm. Additionally, it shows the derivation of a regular grammar from the automaton, reaffirming its position within the Chomsky hierarchy (Type 3). The modular design allows for easy extensions, such as adding graphical representations or further testing.

---


