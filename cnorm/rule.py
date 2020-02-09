from abc import ABCMeta, abstractmethod
from enum import Enum
from itertools import chain
import unicodedata

import jaconv
from word2number.w2n import word_to_num


def is_greek_letter(char: str):
    """determine if the char is Greek character
    see also: https://unicode.org/charts/PDF/U0370.pdf
    :param char:
    :return:
    """
    codes = chain(range(0x370, 0x3e2), range(0x3f0, 0x400))
    symbols = [chr(c) for c in codes]
    letters = [c for c in symbols if c.isalpha()]
    if char in letters:
        return True
    else:
        return False


def get_name_of_greek_letter(char: str):
    """
    caution: return None for "ʹ" (GREEK NUMERAL SIGN) and "ͺ" (GREEK YPOGEGRAMMENI)
    :param char:
    :return:
    """
    name = unicodedata.name(char)
    if 'ARCHAIC' in name:
        return name.split()[-1]
    elif 'PAMPHYLIAN' in name:
        return name.split()[-1]
    elif 'WITH TONOS' in name:
        return name.split()[-3]
    elif 'SYMBOL' in name:
        return name.split()[-2]
    elif 'SMALL LETTER' in name:
        return name.split()[3]
    elif 'CAPITAL LETTER' in name:
        return name.split()[3]
    elif 'LETTER' in name:
        return name.split()[2]
    else:
        return


def is_roman_numeral(char: str):
    """determine if the char is Roman Numeral
    see also: https://unicode.org/charts/PDF/U2150.pdf
    :param char:
    :return:
    """
    codes = range(0x2160, 0x217f)
    symbols = [chr(c) for c in codes]
    if char in symbols:
        return True
    else:
        return False


def get_name_of_roman_numeral(char: str):
    """
    caution: return expression of number
    :param char:
    :return:
    """
    name = unicodedata.name(char)
    name = name.split('ROMAN NUMERAL ')[-1]
    return name


class Case(Enum):
    UPPER = 1
    LOWER = 2


class Form(Enum):
    NFC = 1
    NFKC = 2
    NFD = 3
    NFKD = 4


class Rule(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, text: str):
        pass


class Lower(Rule):
    """convert upper case to lower case
    """

    def __init__(self):
        super(Lower, self).__init__()

    def apply(self, text: str):
        return text.lower()


class Greek2Alpha(Rule):
    """convert Greek char to Alphabet
    caution: "μ" will be converted to "MU" (not "micro")
    ----
    g2a = Greek2Alpha()
    g2a.apply("β ver")  # return "beta ver"
    g2a.apply("50 μg")  # return "50 mug"
    """
    def __init__(self):
        super(Greek2Alpha, self).__init__()

    def apply(self, text: str, case: Case=Case.LOWER):
        char_list = []
        for char in text:
            if is_greek_letter(char):
                char = get_name_of_greek_letter(char)
                if case == Case.LOWER:
                    char = char.lower()
            char_list.append(char)
        return ''.join(char_list)


class RomNum2AraNum(Rule):
    """convert Roman Numeral to Arabic Numeral
    """
    def __init__(self):
        super(RomNum2AraNum, self).__init__()

    def apply(self, text: str, case: Case=Case.LOWER):
        char_list = []
        for char in text:
            if is_roman_numeral(char):
                char = get_name_of_roman_numeral(char)
                if case == Case.LOWER:
                    char = char.lower()
            char_list.append(char)
        return ''.join(char_list)


class Word2Num(Rule):
    """convert numeric word to number
    """
    def __init__(self):
        super(Word2Num, self).__init__()

    def apply(self, text: str):
        """
        see also: https://github.com/akshaynagpal/w2n
        :param text:
        :return:
        """
        word_list = []
        num_list = []
        for word in text.split():
            try:
                word_to_num(word)
                num_list.append(word)
            except ValueError:
                if num_list:
                    word_list.append(
                        str(word_to_num(' '.join(num_list)))
                    )
                word_list.append(word)
                num_list = []
        if num_list:
            word_list.append(
                str(word_to_num(' '.join(num_list)))
            )

        return ' '.join(word_list)


class Normalize(Rule):
    """normalize
    """
    def __init__(self):
        super(Normalize, self).__init__()

    def apply(self, text: str, form: Form=Form.NFKC):
        return unicodedata.normalize(form.name, text)


class NormalizeJaConv(Rule):
    """normalize with jaconv
    dash- and hyphen- like characters are normalized
    """
    def __init__(self):
        super(NormalizeJaConv, self).__init__()

    def apply(self, text: str, form: Form=Form.NFKC):
        return jaconv.normalize(text, form.name)
