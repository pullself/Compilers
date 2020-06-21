from libs.lexers.token import Token
from libs.lexers.tag import Tag


class Real(Token):
    def __init__(self, t: float):
        super(Real, self).__init__(Tag.REAL)
        self.value = t

    def toString(self) -> str:
        return str(self.value)
