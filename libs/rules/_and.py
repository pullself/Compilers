from libs.rules.logical import Logical


class And(Logical):
    def __init__(self, tok, x1, x2):
        super(And, self).__init__(tok, x1, x2)

    def jumping(self, t, f):
        label = f if f != 0 else self.new_label()
        self.expr1.jumping(0, label)
        self.expr2.jumping(t, f)
        if f == 0:
            self.emit_label(label)
