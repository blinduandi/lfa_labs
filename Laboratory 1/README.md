# Formal Languages & Finite Automata Project  
### Teachers  
- **Cretu Dumitru**  
- **Irina Cojuhari**  

### Student  
- **Blindu Andi** FAF-233  

---

## Overview  
This project demonstrates the implementation of a regular grammar and its conversion into a finite automaton. The main objectives are:  
- **Generating Strings:** Create valid strings from a defined grammar  
- **Grammar-to-Automaton Conversion:** Convert the grammar into a finite automaton  
- **String Validation:** Check if a string is accepted by the finite automaton  

For **Variant 2**, the grammar is defined as:  
- **Non-terminals (VN):** `{ S, R, L }`  
- **Terminals (VT):** `{ a, b, c, d, e, f }`  
- **Productions (P):**  
  - `S → aS`  
  - `S → bS`  
  - `S → cR`  
  - `S → dL`  
  - `R → dL`  
  - `R → e`  
  - `L → fL`  
  - `L → eL`  
  - `L → d`  

# String Generation Implementation

The system starts with an initial symbol `S` and evolves the string by applying production rules. At each step, a production rule is chosen at random until the string reaches a terminal state. This method strikes a balance between structure and randomness, ensuring predictable patterns with a touch of surprise.

Additionally, an optional mode allows for generating invalid strings by deliberately appending characters that deviate from the established grammar, based on probabilistic criteria. This feature adds flexibility by enabling controlled deviations from strict grammatical rules.

Overall, the approach is both reliable and adaptable, making it suitable for testing, simulating language patterns, or any scenario that benefits from dynamic string synthesis.


### 2. Grammar-to-Automaton Conversion  
```python
 
def to_finite_automaton():
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
```
**Explanation:**  
- **Purpose:** Creates equivalent finite automaton from grammar  
- **Conversion Logic:**  
  - Non-terminals become states  
  - Added final state `F` for termination  
  - Productions mapped to transition rules  
- **Key Rules:**  
  - `A → xB` becomes transition `A → B on x`  
  - `A → x` becomes transition `A → F on x`  

---

### 3. String Validation Mechanism  
```python
def string_belongs_to_language(self, input_string):
    current_state = self.start_state
    for symbol in input_string:
        if symbol not in self.alphabet:
            return False
        if symbol not in self.transitions[current_state]:
            return False
        current_state = self.transitions[current_state][symbol]
    return current_state in self.final_states
 ```   
**Explanation:**

The automaton is designed to verify if a string is accepted. It starts at the initial state `S` and processes symbols one by one using a transition table. As each symbol is read, the automaton ensures that a valid transition exists. After processing, it checks whether the final state is acceptable. The process fails if an invalid symbol is encountered, if a necessary transition is missing, or if the final state is not an accepting state.


## Summary of Implementation

The implementation achieves several core objectives: it delivers a functional grammar string generator, enables bi-directional conversion between grammar and automaton, and establishes a complete validation pipeline. This framework draws strong parallels between its components, mapping productions to transitions, non-terminals to states, and terminal symbols to the alphabet. In practical terms, these capabilities support language membership testing, automated test case generation, and the verification of grammar and automaton equivalence.


