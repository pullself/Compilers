from libs.rules.expr import Expr
from libs.symbols.type import Type, Types


class Unary(Expr):
    def __init__(self, tok, x):
        super(Unary, self).__init__(tok, None)
        self.expr = x
        self.type = Type.max(Types.Int, self.expr.type)
        if self.type == None:
            self.error('type error')

    def gen(self):
        return Unary(self.op, self.expr.reduce())

    def toString(self):
        return self.op.toString()+' '+self.expr.toString()
