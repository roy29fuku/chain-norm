from typing import List

from cnorm.rule import Rule


class Chain(object):
    """
    the chain of rules
    """
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def apply(self, text: str):
        for rule in self.rules:
            text = rule.apply(text)
        return text
