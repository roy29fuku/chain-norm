from typing import List

from cnorm.rule import Rule


class Chain(object):
    """
    the chain of rules
    """
    def __init__(self, rules: List[Rule]=None):
        self.rules = rules

    def apply(self, text: str):
        if self.rules is None:
            return text
        for rule in self.rules:
            text = rule.apply(text)
        return text
