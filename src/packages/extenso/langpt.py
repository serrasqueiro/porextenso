# -*- coding: iso-8859-1 -*-
# langpt.py  (c)2021  Henrique Moreira

""" langpt - display money in an extended way

Compatibility: python 3.
"""

# pylint: disable=missing-function-docstring

from extenso.amoney import Money

PT_NUM = {
    0: "zero",
    1: "um",
    2: "dois",
    3: "tres",
    4: "quatro",
    5: "cinco",
    6: "seis",
    7: "sete",
    8: "oito",
    9: "nove",
    10: "dez",
    11: "onze",
    12: "doze",
    13: "treze",
    14: "catorze",
    15: "quinze",
    16: "dezasseis",
    17: "dezasete",
    18: "dezoito",
    19: "dezanove",
    20: "vinte",
    30: "trinta",
    40: "quarenta",
    50: "cinquenta",
    60: "sessenta",
    70: "setenta",
    80: "oitenta",
    90: "noventa",
    100: "cem",
    200: "duzentos",
    300: "trezentos",
    400: "quatrocentos",
    500: "quinhentos",
    600: "seiscentos",
    700: "setecentos",
    800: "oitocentos",
    900: "novecentos",
    1000: "mil",
}

def basic_test():
    """ Just a basic class test! """
    for ranges in (
            (1, 9), (10, 102), (110, 121),
            (200, 231), (300, 331), (900, 1003),
            (1151, 1161), (19000, 19001),
            (20000, 20021), (900000, 0), (990234, 0),
            (10 ** 6, 10 ** 6 + 3), (10 ** 6 + 100, 10 ** 6 + 21),
            (8 * 10 ** 6, 0), (97 * 10 ** 6, 0),
            (12456789, 0),
            (123 * 10 ** 6, 0),  # returns '?'
    ):
        range_min, range_max = ranges
        for num in range(range_min, range_max+1 if range_max else range_min+1):
            aval = float(num)
            new = Euro(aval)
            shown = new.long_str()
            print(f"{new.value():0.2f} ({shown})")
            assert shown.strip() == shown, f"Uops: '{shown}'"
            assert new.value() != 0.0


class Euro(Money):
    """ My money as euro
    """
    def __init__(self, value=0.0, bystr:str=""):
        super().__init__(value, bystr)
        self._coin_str = "Euro"

    def long_str(self) -> str:
        return self.value_pt()

    def value_pt(self) -> str:
        return self._my_value_str(self._value)

    def _my_value_str(self, aval:float) -> str:
        astr = ""
        uval = abs(aval)
        coin = f" {self._coin_str}"
        if aval == 0.0:
            return f"0{coin}"
        assert uval >= 0.01
        if aval < 0:
            return "-" + self._my_value_str(-aval)
        ival = int(uval)
        if ival > 100 * 10 ** 6:
            return "?"
        newval = ival // (10 ** 6)
        if newval:
            modus = ival % 10 ** 6
            if astr:
                astr += ", "
            if newval > 1:
                suffix = "milhões"
                singular = modus < 100000
            else:
                singular = modus == 0
                suffix = "mihão"
            what = self._zero_cem(newval)
            if not astr:
                what = what.capitalize()
            astr += f"{what} {suffix}"
            if singular:
                astr += " de"  # Um milhão 'de' Euros
            ival -= newval * (10 ** 6)
        newval = ival // (10 ** 3)
        if newval:
            suffix = "mil" if newval > 1 else "Mil"
            there = self._zero_mil(ival)
            if astr:
                astr += ", "
            if not astr:
                there = there.capitalize()
            if newval > 1:
                astr += there + f" {suffix}"
            else:
                astr += suffix
            ival -= newval * (10 ** 3)
        newval = ival // 100
        if newval:
            what = PT_NUM.get(newval * 100)
            ival -= newval * 100
            if what is None:
                there = ""
            else:
                there = what if newval != 1 else "cento"
            if not astr:
                there = there.capitalize()
            if astr:
                astr += ", "
            astr += there
        there = self._zero_cem(ival)
        if there and ival:
            if astr:
                astr += " e "
            astr += there
        # finally, sigh!
        suffix = "" if int(aval) == 1 else "s"
        astr += coin + suffix
        cents = int(uval * 100.0) - int(uval) * 100
        assert 0 <= cents < 100
        if not cents:
            return astr
        suffix = "s" if cents > 1 else ""
        astr += " e " + self._zero_cem(cents) + " centimo" + suffix
        return astr

    def _zero_cem(self, ival) -> str:
        newval = ival // 10
        if ival < 20:
            # teenager statement
            return PT_NUM[ival]
        what = PT_NUM.get(newval * 10)
        if ival % 10:
            a_decimal = PT_NUM[ival % 10]
            there = f"{what} e {a_decimal}"
        else:
            assert what, f"zero_cem({ival}), PT_NUM: {newval * 10}"
            there = what
        return there

    def _zero_mil(self, ival) -> str:
        assert ival <= 10 ** 6
        newval = ival // 1000
        if newval < 100:
            what = self._zero_cem(newval)
        else:
            centos = newval // 100
            what = PT_NUM.get(newval)
            if what is None:
                # e.g. 234, 'duzentos e trinta e quatro'
                what = PT_NUM[centos * 100]
            if centos * 100 == newval:
                return what
            what += " e " + self._zero_cem(newval - centos * 100)
        return what

if __name__ == "__main__":
    print("Please import me")
    basic_test()
