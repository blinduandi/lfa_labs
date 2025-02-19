# Formal Languages & Finite Automata Project

### Teachers
- **Cretu Dumitru**
- **Irina Cojuhari**
### Student
- **Blindu Andi** FAF-233

---

## Overview

This project serves as an introduction to formal languages and finite automata. The assignment involves:
- Defining a regular grammar.
- Generating valid strings from the grammar.
- Converting the grammar into an equivalent finite automaton.
- Testing whether given strings belong to the language of the finite automaton.

### The Grammar

For **Variant 2**, the grammar is defined as follows:

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

### Implementation Details

1. **Grammar Class:**
   - **State Variables:**  
     - `non_terminals`, `terminals`, `start_symbol`, and `productions`
   - **Methods:**
     - `generate_string()`: Uses random selection of productions to generate valid strings.
     - `to_finite_automaton()`: Converts the regular grammar into a Finite Automaton by mapping productions to transitions. 
       - For a production of the form `A → xB`, a transition from state `A` to state `B` on symbol `x` is created.
       - For a production of the form `A → x`, a transition from state `A` to a new final state `F` is created.

2. **Finite Automaton Class:**
   - **State Variables:**  
     - `states`, `alphabet`, `transitions`, `start_state`, and `final_states`
   - **Methods:**
     - `string_belongs_to_language(input_string)`: Simulates the FA transitions on the input string and determines if it is accepted (i.e., it ends in a final state).

3. **Usage:**
   - The main section of the script demonstrates generating 5 valid strings from the grammar.
   - It converts the grammar to a finite automaton and tests 5 strings to check if they belong to the language.


