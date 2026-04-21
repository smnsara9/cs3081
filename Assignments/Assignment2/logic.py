# ============================================================
# logic.py  –  Helper file for CS3081 Lab 2 Part 2
# DO NOT MODIFY THIS FILE
# ============================================================
# This file provides the basic building blocks for
# propositional logic in Python.
# ============================================================

class Sentence:
    """Base class for all logical sentences."""
    pass


class Symbol(Sentence):
    """A propositional symbol  (e.g., Rain, Sunny, Guilty)."""
    def __init__(self, name):
        self.name = name

    def evaluate(self, model):
        # Look up this symbol's truth value in the model
        return model.get(self.name, False)

    def __repr__(self):
        return self.name


class Not(Sentence):
    """Negation:  NOT(operand)"""
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def __repr__(self):
        return f"NOT({self.operand})"


class And(Sentence):
    """Conjunction:  AND(a, b, ...)"""
    def __init__(self, *conjuncts):
        self.conjuncts = list(conjuncts)

    def evaluate(self, model):
        return all(c.evaluate(model) for c in self.conjuncts)

    def __repr__(self):
        return f"AND({', '.join(str(c) for c in self.conjuncts)})"


class Or(Sentence):
    """Disjunction:  OR(a, b, ...)"""
    def __init__(self, *disjuncts):
        self.disjuncts = list(disjuncts)

    def evaluate(self, model):
        return any(d.evaluate(model) for d in self.disjuncts)

    def __repr__(self):
        return f"OR({', '.join(str(d) for d in self.disjuncts)})"


class Implication(Sentence):
    """Implication:  IF antecedent THEN consequent"""
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model):
        # P → Q  is false ONLY when P is True and Q is False
        if self.antecedent.evaluate(model) and not self.consequent.evaluate(model):
            return False
        return True

    def __repr__(self):
        return f"IF {self.antecedent} THEN {self.consequent}"


# ============================================================
# Knowledge Base
# ============================================================

class KB:
    """A knowledge base holds a list of sentences we know to be true."""
    def __init__(self):
        self.sentences = []

    def tell(self, sentence):
        """Add a sentence to the knowledge base."""
        self.sentences.append(sentence)

    def evaluate(self, model):
        """Return True only if ALL sentences in the KB are true in this model."""
        return all(s.evaluate(model) for s in self.sentences)


# ============================================================
# Model Checking (check_all)
# ============================================================

import itertools

def check_all(kb, query, symbols):
    """
    Returns True if the query is ENTAILED by the knowledge base.

    How it works:
      1. Generate ALL possible truth-value combinations for the symbols.
      2. For each combination (a "model"):
         - If the KB is TRUE in this model...
         - ...then the query must ALSO be true.
      3. If we find any model where KB is true but query is false → NOT entailed.
    """
    # Build all possible True/False combinations
    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        # Only check models where the KB is satisfied
        if kb.evaluate(model):
            if not query.evaluate(model):
                # Found a counterexample – query is NOT entailed
                return False

    # All KB-consistent models also satisfy the query
    return True
