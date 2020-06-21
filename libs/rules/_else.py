from libs.rules.stmt import Stmt
from libs.symbols.type import Types

class Else(Stmt):
    def __init__(self,x,s1,s2):
        super(Else,self).__init__()
        self.expr = x
        self.stmt1 = s1
        self.stmt2 = s2
        if self.expr.type != Types.Bool:
            self.expr.error('boolean required in if')

    def gen(self,b,a):
        label1 = self.new_label()
        label2 = self.new_label()
        self.expr.jumping(0,label2)
        self.emit_label(label1)
        self.stmt1.gen(label1,a)
        self.emit('goto L'+str(a))
        self.emit_label(label2)
        self.stmt2.gen(label2,a)