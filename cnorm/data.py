from abc import ABCMeta, abstractmethod
from typing import List


class Rule(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, text: str):
        pass


class RuleLower(Rule):
    """
    lower
    """

    def __init__(self):
        super(RuleLower, self).__init__()

    def apply(self, text: str):
        return text.lower()


class RuleHalfWidth(Rule):
    """
    halfwidth
    """
    def __init__(self):
        super(RuleHalfWidth, self).__init__()

    def apply(self, text: str):
        return text.lower()


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
