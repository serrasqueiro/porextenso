# amoney.py  (c)2021  Henrique Moreira

""" amoney - display money in an extended way

Compatibility: python 3.
"""

# pylint: disable=missing-function-docstring


class Money():
    """ My money as string
    """
    _str = ""
    _value = 0.0
    _coin_str = ""

    def __init__(self, value=0.0, bystr:str=""):
        if bystr:
            self._str = bystr
            self._value = float(bystr)
        else:
            assert not bystr
            bystr = f"{value:2.0}"
            self._value = value
        self._str = bystr

    def tostring(self) -> str:
        return self._str

    def value(self) -> float:
        return self._value

    def __str__(self) -> str:
        return self.tostring()

if __name__ == "__main__":
    print("Please import me")
