from libs.rules.stmt import Stmt, Stmts


class Seq(Stmt):
    def __init__(self, s1, s2):
        self.stmt1 = s1
        self.stmt2 = s2

    def gen(self, b, a):
        if self.stmt1 == Stmts.Null:
            self.stmt2.gen(b, a)
        elif self.stmt2 == Stmts.Null:
            self.stmt1.gen(b, a)
        else:
            label = self.new_label()
            self.stmt1.gen(b, label)
            self.emit_label(label)
            self.stmt2.gen(label, a)
