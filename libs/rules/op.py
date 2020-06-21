from libs.rules.expr import Expr
from libs.rules.temp import Temp


class Op(Expr):
    def __init__(self, tok, p):
        super(Op, self).__init__(tok, p)

    def reduce(self):
        x = self.gen()
        t = Temp(self.type)
        self.emit(t.toString()+' = '+x.toString())
        return t
