from libs.lexers.word import Word
from libs.lexers.tag import Tag


class Type(Word):
    def __init__(self, s: str, tag: int, w: int):
        super(Type, self).__init__(s, tag)
        self.width = w

    @staticmethod
    def numeric(p) -> bool:
        if p == Types.Int or p == Types.Float or p == Types.Char:
            return True
        else:
            return False

    @classmethod
    def max(cls, p1, p2):
        if not cls.numeric(p1) or not cls.numeric(p2):
            return None
        elif p1 == Types.Float or p2 == Types.Float:
            return Types.Float
        elif p1 == Types.Int or p2 == Types.Int:
            return Types.Int
        else:
            return Types.Char


class Types():
    Int = Type('int', Tag.BASIC, 8)
    Float = Type('float', Tag.BASIC, 4)
    Char = Type('char', Tag.BASIC, 1)
    Bool = Type('bool', Tag.BASIC, 1)
    count = 4
