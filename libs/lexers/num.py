from libs.lexers.token import Token
from libs.lexers.tag import Tag

class Num(Token):
    def __init__(self, t: int):
        super(Num, self).__init__(Tag.NUM)
        self.value = t

    def toString(self) -> str:
        return str(self.value)


