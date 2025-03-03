# Determinism in Finite Automata: NDFA to DFA Conversion and Regular Grammar Derivation

**Course:** Formal Languages & Finite Automata  
**Author:** Cretu Dumitru  
**Acknowledgments:** Kudos to Vasile Drumea and Irina Cojuhari\
**Student:** Blindu Andi FAF-233

---

## 1. Introduction

Finite automata are abstract machines that play a key role in the study of formal languages and computation by modeling processes with a finite number of states. In this project, the focus is on verifying whether a given automaton is deterministic or non-deterministic, converting a non-deterministic finite automaton (NDFA) to a deterministic finite automaton (DFA) using the subset construction algorithm, and deriving the equivalent regular grammar (right-linear grammar) from the finite automaton. This derivation confirms the automaton's position within the Chomsky hierarchy as a Type 3 grammar.


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

In deterministic finite automata (DFA), every state has exactly one transition for each input symbol, ensuring that each input leads to a unique computational path. Conversely, non-deterministic finite automata (NDFA) allow states to have multiple transitions for the same input, which can result in several possible computation paths. It is well established that every NDFA can be converted into an equivalent DFA.

### 3.2 Subset Construction Algorithm

The conversion from an NDFA to a DFA is achieved using the subset construction algorithm. This process starts by defining the DFA's initial state as the set that contains the NDFA’s start state (e.g., \(\{q0\}\)). Then, for each DFA state, which represents a set of NDFA states, and for each symbol in the alphabet, the algorithm computes the union of transitions from those NDFA states. Each resulting union forms a new DFA state if it has not been previously encountered. Finally, any DFA state that contains at least one NDFA final state is marked as accepting, ensuring that the DFA accurately represents the language of the original NDFA.

### 3.3 Conversion to Regular Grammar

Finite automata can also be translated into a regular (right-linear) grammar. This conversion involves creating production rules from the automaton's transitions. For every transition \( Δ(q_i, a) = q_j \), a production rule \( A_i \rightarrow aA_j \) is defined, where \( A_i \) and \( A_j \) correspond to the automaton states \( q_i \) and \( q_j \), respectively. Additionally, for each final state \( q_f \), an epsilon production \( A_f \rightarrow \epsilon \) is added to permit the termination of derivations. This results in a regular grammar that is equivalent in expressive power to the original automaton.

---

## 4. Implementation

The project is implemented in Python and is organized into two main components. The first component is the FiniteAutomaton class, which encapsulates the functionality of a nondeterministic finite automaton (NDFA). This class defines the NDFA structure, provides a method to check whether the automaton is deterministic, and implements the subset construction algorithm to convert an NDFA into a DFA. Additionally, it includes a method to derive the equivalent regular grammar from the automaton, linking the concepts of grammar and automata.

The second component is the DFA class. This class represents the deterministic finite automaton that results from the conversion process. It includes methods for presenting the DFA in a structured and formatted manner, ensuring that the output is clear and easy to interpret. Together, these classes support a comprehensive pipeline for grammar and automaton conversion, validation, and analysis.

### 4.1 Code


```python
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

```

## 5. Testing and Results

When executed, the program performs several key tasks. First, it checks the determinism of the original automaton, confirming that it is nondeterministic (for instance, state `q1` has two transitions on symbol `b`). Next, the subset construction algorithm converts the NDFA to a DFA. In this conversion, DFA states are represented as sets of NDFA states, and the transitions are adjusted accordingly. Finally, the program derives a right-linear grammar from the automaton. The production rules are based on the transitions, with epsilon productions added for final states. The results verify that the conversion processes function correctly and that the derived regular grammar faithfully represents the language of the original automaton.


## 6. Conclusion

This project demonstrates the conversion of a non-deterministic finite automaton into a deterministic one using the subset construction algorithm. Additionally, it shows the derivation of a regular grammar from the automaton, reaffirming its position within the Chomsky hierarchy (Type 3). The modular design allows for easy extensions, such as adding graphical representations or further testing.

---


