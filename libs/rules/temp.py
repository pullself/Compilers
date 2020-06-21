from libs.rules.expr import Expr
from libs.symbols.type import Type
from libs.lexers.word import Words


class Temp(Expr):
    count = 0

    def __init__(self, p: Type):
        super(Temp, self).__init__(Words.temp, p)
        Temp.count += 1
        self.number = Temp.count

    def toString(self):
        return 't'+str(self.number)
