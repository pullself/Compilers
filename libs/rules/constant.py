from libs.rules.expr import Expr
from libs.symbols.type import Types
from libs.lexers.num import Num
from libs.lexers.word import Words


class Constant(Expr):
    def __init__(self, tok, p=None):
        if isinstance(tok, int):
            super(Constant, self).__init__(Num(tok), Types.Int)
        else:
            super(Constant, self).__init__(tok, p)

    def jumping(self, t, f):
        if self is Constants.true and t != 0:
            self.emit('goto L'+str(t))
        elif self is Constants.false and f != 0:
            self.emit('goto L' + str(f))


class Constants:
    true = Constant(Words.true, Types.Bool)
    false = Constant(Words.false, Types.Bool)
