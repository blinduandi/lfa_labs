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

---

## Key Components and Explanations  

### 1. String Generation Implementation  
*Code implementation for string generation will be inserted here*  

**Explanation:**  
- **Purpose:** Generates strings starting from `S` through random production selection  
- **Features:**  
  - Builds strings until terminal production is reached  
  - Optional invalid string generation mode  
  - Probabilistic invalid character append  
- **Mechanism:**  
  - Iterative production rule application  
  - Random choice at each derivation step  

---

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
- **Purpose:** Checks string acceptance by automaton  
- **Validation Process:**  
  1. Starts at initial state `S`  
  2. Processes symbols sequentially  
  3. Follows transition table  
  4. Verifies final state  
- **Failure Conditions:**  
  - Invalid symbol detection  
  - Missing transition path  
  - Non-final end state  

---

## Summary of Implementation  
- **Core Achievements:**  
  - Functional grammar string generator  
  - Bi-directional grammar-automaton conversion  
  - Complete validation pipeline  

- **Key Relationships:**  
  - Productions ↔ Transitions  
  - Non-terminals ↔ States  
  - Terminal symbols ↔ Alphabet  

- **Practical Applications:**  
  - Language membership testing  
  - Automated test case generation  
  - Grammar/automaton equivalence verification  

This implementation provides concrete examples of formal language concepts, demonstrating the theoretical foundations through practical computational methods.