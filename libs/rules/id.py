from libs.rules.expr import Expr
from libs.lexers.word import Word
from libs.symbols.type import Type


class Id(Expr):
    def __init__(self, _id: Word, p: Type, b: int):
        super(Id, self).__init__(_id, p)
        self.offset = b
