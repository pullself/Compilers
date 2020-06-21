from libs.rules.logical import Logical
from libs.symbols.array import Array
from libs.symbols.type import Types


class Rel(Logical):
    def __init__(self, tok, x1, x2):
        super(Rel, self).__init__(tok, x1, x2)

    def check(self, p1, p2):
        # 不允许强制类型转换
        if isinstance(p1, Array) or isinstance(p2, Array):
            return None
        elif p1 == p2:
            return Types.Bool
        else:
            return None

    def jumping(self, t, f):
        a = self.expr1.reduce()
        b = self.expr2.reduce()
        test = a.toString()+' '+self.op.toString()+' '+b.toString()
        self.emitjumps(test, t, f)
