from abc import ABCMeta, abstractmethod
from enum import Enum
import unicodedata

import jaconv
from word2number.w2n import word_to_num


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
    see also: https://unicode.org/charts/PDF/U0370.pdf
    """
    def __init__(self):
        super(Greek2Alpha, self).__init__()

    def apply(self, text: str):
        # Letters (0x0386, 0x0388-0x03CE)
        ## GREEK CAPITAL LETTER
        text = text.replace('Α', 'ALPHA').replace('Β', 'BETA').replace('Γ', 'GAMMA').replace('Δ', 'DELTA')
        text = text.replace('Ε', 'EPSILON').replace('Ζ', 'ZETA').replace('Η', 'ETA').replace('Θ', 'THETA')
        text = text.replace('Ι', 'IOTA').replace('Κ', 'KAPPA').replace('Λ', 'LAMDA').replace('Μ', 'MU')
        text = text.replace('Ν', 'NU').replace('Ξ', 'XI').replace('Ο', 'OMICRON').replace('Π', 'PI')
        text = text.replace('Ρ', 'RHO').replace('Σ', 'SIGMA').replace('Τ', 'TAU').replace('Υ', 'UPSILON')
        text = text.replace('Φ', 'PHI').replace('Χ', 'CHI').replace('Ψ', 'PSI').replace('Ω', 'OMEGA')
        ## GREEK CAPITAL LETTER WITH DIALYTIKA
        text = text.replace('Ϊ', 'IOTA').replace('Ϋ', 'UPSILON')
        ## GREEK CAPITAL LETTER WITH TONOS
        text = text.replace('Ά', 'ALPHA').replace('Έ', 'EPSILON').replace('Ή', 'ETA').replace('Ί', 'IOTA')
        text = text.replace('Ό', 'OMICRON').replace('Ύ', 'UPSILON').replace('Ώ', 'OMEGA').replace('ΐ', 'IOTA')
        ## GREEK SMALL LETTER
        text = text.replace('α', 'alpha').replace('β', 'beta').replace('γ', 'gamma').replace('δ', 'delta')
        text = text.replace('ε', 'epsilon').replace('ζ', 'zeta').replace('η', 'eta').replace('θ', 'theta')
        text = text.replace('ι', 'iota').replace('κ', 'kappa').replace('λ', 'lamda').replace('μ', 'mu')
        text = text.replace('ν', 'nu').replace('ξ', 'xi').replace('ο', 'omicron').replace('π', 'pi')
        text = text.replace('ρ', 'rho').replace('ς', 'sigma').replace('σ', 'sigma').replace('τ', 'tau').replace('υ', 'upsilon')
        text = text.replace('φ', 'phi').replace('χ', 'chi').replace('ψ', 'psi').replace('ω', 'omega')
        ## GREEK SMALL LETTER WITH DIALYTIKA
        text = text.replace('ά', 'alpha').replace('έ', 'epsilon').replace('ή', 'eta').replace('ί', 'iota')
        text = text.replace('ϊ', 'iota').replace('ϋ', 'upsilon')
        ## GREEK SMALL LETTER WITH TONOS
        text = text.replace('ό', 'omicron').replace('ύ', 'upsilon').replace('ώ', 'omega')
        ## GREEK SMALL LETTER WITH DIALYTIKA AND TONOS
        text = text.replace('ΰ', 'upsilon')

        # Additional letters (0x037F, 0x03F3)
        text = text.replace('Ϳ', 'YOT').replace('ϳ', 'yot')

        # Variant letterforms (0x03CF-0x03D7, 0x03F0-0x03F2, 0x03F4-0x03F6, 0x03F9)
        text = text.replace('Ϗ', 'kai').replace('ϐ', 'beta').replace('ϑ', 'theta').replace('ϒ', 'upsilon')
        text = text.replace('ϓ', 'upsilon').replace('ϔ', 'upsilon').replace('ϕ', 'phi').replace('ϖ', 'pi')
        text = text.replace('ϗ', 'kai')
        text = text.replace('ϰ', 'kappa').replace('ϱ', 'rho').replace('ϲ', 'sigma')
        text = text.replace('ϴ', 'THETA').replace('ϵ', 'epsilon').replace('϶', 'epsilon')
        text = text.replace('Ϲ', 'SIGMA')

        # Archaic letters (0x0370-0x0373, 0x0376-0x0377, 0x03D8-0x03E1, 0x03FA-0x03FB)
        text = text.replace('Ͱ', 'HETA').replace('ͱ', 'heta').replace('Ͳ', 'SAMPI').replace('ͳ', 'sampi')
        text = text.replace('Ͷ', 'PAMPHYLIAN').replace('ͷ', 'pamphylian')
        text = text.replace('Ϙ', 'KOPPA').replace('ϙ', 'koppa').replace('Ϛ', 'SIGMA').replace('ϛ', 'sigma')
        text = text.replace('Ϝ', 'DIGAMMA').replace('ϝ', 'digamma').replace('Ϟ', 'KOPPA').replace('ϟ', 'koppa')
        text = text.replace('Ϡ', 'SAMPI').replace('ϡ', 'sampi')
        text = text.replace('Ϻ', 'SAN').replace('ϻ', 'san')

        # Additional archaic letters for Bactrian (0x03F7-0x03F8)
        text = text.replace('Ϸ', 'SHO').replace('ϸ', 'sho')

        # Symbol (0x03FC-0x03FF)
        text = text.replace('ϼ', 'rho').replace('Ͻ', 'SIGMA').replace('Ͼ', 'SIGMA').replace('Ͽ', 'SIGMA')

        return text


class RomNum2AraNum(Rule):
    """convert Roman Numeral to Arabic Numeral
    see also: https://unicode.org/charts/PDF/U2150.pdf
    """
    def __init__(self):
        super(RomNum2AraNum, self).__init__()

    def apply(self, text: str, case: Case=Case.LOWER):
        # Roman numerals (0x2160-0x217f)
        text = text.replace('Ⅰ', 'ONE').replace('Ⅱ', 'TWO').replace('Ⅲ', 'THREE').replace('Ⅳ', 'FOUR')
        text = text.replace('Ⅴ', 'FIVE').replace('Ⅵ', 'SIX').replace('Ⅶ', 'SEVEN').replace('Ⅷ', 'EIGHT')
        text = text.replace('Ⅸ', 'NINE').replace('Ⅹ', 'TEN').replace('Ⅺ', 'ELEVEN').replace('Ⅻ', 'TWELVE')
        text = text.replace('Ⅼ', 'FIFTY').replace('Ⅽ', 'ONE HUNDRED').replace('Ⅾ', 'FIVE HUNDRED').replace('Ⅿ', 'ONE THOUSAND')
        text = text.replace('ⅰ', 'one').replace('ⅱ', 'two').replace('ⅲ', 'three').replace('ⅳ', 'four')
        text = text.replace('ⅴ', 'five').replace('ⅵ', 'six').replace('ⅶ', 'seven').replace('ⅷ', 'eight')
        text = text.replace('ⅸ', 'nine').replace('ⅹ', 'ten').replace('ⅺ', 'eleven').replace('ⅻ', 'twelve')
        text = text.replace('ⅼ', 'fifty').replace('ⅽ', 'one hundred').replace('ⅾ', 'five hundred').replace('ⅾ', 'one thousand')
        return text

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
