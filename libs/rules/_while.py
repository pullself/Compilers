from libs.rules.stmt import Stmt
from libs.symbols.type import Types


class Whlie(Stmt):
    def __init__(self):
        super(Whlie, self).__init__()
        self.expr = None
        self.stmt = None

    def init(self, x, s):
        self.expr = x
        self.stmt = s
        if self.expr.type != Types.Bool:
            self.expr.error('boolean required in while')

    def gen(self, b, a):
        self.after = a
        self.expr.jumping(0, a)
        label = self.new_label()
        self.emit_label(label)
        self.stmt.gen(label, b)
        self.emit('goto L'+str(b))
