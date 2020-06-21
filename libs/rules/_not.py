from libs.rules.logical import Logical


class Not(Logical):
    def __init__(self, tok, x):
        super(Not, self).__init__(tok, x, x)

    def jumping(self, t, f):
        self.expr2.jumping(f, t)

    def toString(self):
        return self.op.toString()+' '+self.expr2.toString()
