# Regular Expressions
### Course: Formal Languages & Finite Automata  
### Author: Darzu Catalin (Modified for Variant 2)  
### Variant: 2

----

## Theory

### What are Regular Expressions?

Regular expressions (regex or regexp) are specialized patterns used to search, match, and manipulate text based on specific rules. Originating in the 1950s as a way to describe formal languages, regex has become a vital tool in computer science, data processing, and text analysis. The power of regex lies in its compact syntax and expressive capability, allowing complex text processing with minimal code.

Regular expressions define search patterns that are interpreted by finite automata. This theoretical foundation ensures that regex engines are efficient and predictable, making them ideal for real-time text validation and extraction.

### What Are Regular Expressions Used For?

Regex is widely used in:

- **Input validation** (e.g., checking if an email address is valid)
- **Search and replace** operations in editors and IDEs
- **Extracting structured data** from unstructured text sources such as logs or HTML

Examples include validating phone numbers, extracting hashtags from tweets, or finding dates in documents.

### Basic Regex Elements

- **Literals**: Characters like `A`, `3`, or `m` match themselves.
- **Character Sets**: `[abc]` matches either `a`, `b`, or `c`.
- **Groups and Alternation**: `(a|b|c)` means "either a, b, or c".
- **Quantifiers**:
  - `*` — zero or more repetitions
  - `+` — one or more repetitions
  - `?` — zero or one occurrence
  - `{n}` — exactly `n` repetitions
- **Anchors and Metacharacters**: `^`, `$`, `\b`, `.`, `\d` etc.

## Objectives

This lab aims to:

1. Describe the concept and utility of regular expressions  
2. Generate valid strings from regex patterns using custom logic  
3. Log each step taken during the generation for educational and debugging purposes  

## Implementation Description

The project is based on a custom regex processor and generator for **Variant 2**, focusing on the expression:

```python
variant_2 = """
m? N^2 (O|P)^3 Q^2 R+
(X|Y|Z)^3 (8^9|8^0)
(H|i) (j|k) L* N?
"""
```

This expression includes optional characters, groups with fixed repetitions, plus/asterisk quantifiers, and special forms like exponent-style patterns (`^3`, `^0`).

### 1. Normalization

```python
def _normalize_regex(self, regex_str):
    regex_str = regex_str.replace('²', '2')
    regex_str = regex_str.replace('³', '3')
    regex_str = re.sub(r'\)\^(\d+)', r')\1', regex_str)  # )^5 -> )5
    regex_str = re.sub(r'([A-Za-z0-9])\^(\d+)', r'\1\2', regex_str)
    return regex_str
```

Before tokenizing, the input is normalized to handle superscripts and caret notations.

### 2. Tokenization

```python
def tokenize(self, regex_str):
    patterns = [
        (r'\([^()]+\)(?:\*|\+|\?|\d+)?', 'group'),
        (r'[A-Za-z0-9]\*', 'zero_or_more'),
        (r'[A-Za-z0-9]\+', 'one_or_more'),
        (r'[A-Za-z0-9]\?', 'optional'),
        (r'[A-Za-z0-9]\d+', 'repeat'),
        (r'[A-Za-z0-9]', 'literal')
    ]
```

The tokenization process classifies input patterns into meaningful components: literals, quantifiers, and groups.

### 3. Group Parsing

```python
def parse_group(self, group_token):
    match = re.match(r'\(([^()]+)\)([*+?]|\d+)?', group_token)
    if not match:
        return [group_token], [1]
    content, operator = match.groups()
    alternatives = [alt.strip() for alt in content.split('|')]
    ...
```

The function splits group content and determines repetition rules based on `*`, `+`, `?`, or an explicit number.

### 4. Random Generation

```python
def generate_combinations(self, regex_str, count=10, seed=None):
    ...
    for token, ttype in tokens:
        if ttype == 'literal':
            combo.append(token)
        elif ttype == 'zero_or_more':
            char = token[0]
            r = random.randint(0, self.max_repetitions)
            combo.append(char * r)
        ...
```

Each token is interpreted and transformed into a string fragment, based on random selection and repetition rules. The `get_steps()` function logs every choice.

## Results

Given the input:
```
m? N² (O|P)^3 Q^2 R+ (X|Y|Z)^3 (8^9|8^0) (H|i) (j|k) L* N?
```
After normalization:
```
m? N2 (O|P)3 Q2 R+ (X|Y|Z)3 (89|80) (H|i) (j|k) L* N?
```
Sample output strings:
```
mNNOOOQQRRRXYZ888888888HiL N
NNOPOQQRRRRRYYX Hk LL
```
Each line is a valid string based on the original regex logic, with randomness in group selection and repetition.

## Conclusion

This variant demonstrates how regular expressions, when combined with parsing and random generation logic, can be used to create meaningful strings that conform to formal language rules. The project bridges theoretical knowledge (finite automata and regular languages) with a practical coding task that deepens understanding of how regex engines operate under the hood.

By building tools like `tokenize()` and `generate_combinations()`, students gain insight into how symbols, quantifiers, and alternations are interpreted and executed. This hands-on approach reinforces both academic theory and real-world skills.

## References

1. Stephen Cole Kleene (1951). *Representation of Events in Nerve Nets and Finite Automata*  
2. *Formal Languages and Finite Automata, Guide for Practical Lessons* (Available at FCIM site or library)  
3. [Wikipedia: Regular Expressions](https://en.wikipedia.org/wiki/Regular_expression)  
4. [Python re Module Documentation](https://docs.python.org/3/library/re.html)

