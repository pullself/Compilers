from libs.rules.expr import Expr
from libs.symbols.type import Types
from libs.rules.temp import Temp


class Logical(Expr):
    def __init__(self, tok, x1, x2):
        super(Logical, self).__init__(tok, None)
        self.expr1 = x1
        self.expr2 = x2
        self.type = self.check(self.expr1.type, self.expr2.type)
        if self.type == None:
            self.error('type error')

    def check(self, p1, p2):
        # 只接受bool类型
        if p1 is Types.Bool and p2 is Types.Bool:
            return Types.Bool
        else:
            return None

    def gen(self):
        # 是否写成reduce更好（pass）
        f = self.new_label()
        a = self.new_label()
        temp = Temp(self.type)
        self.jumping(0,f)
        self.emit(temp.toString()+' = true')
        self.emit('goto L'+str(a))
        self.emit_label(f)
        self.emit(temp.toString()+' = false')
        self.emit_label(a)
        return temp

    def toString(self):
        return self.expr1.toString()+' '+self.op.toString()+' '+self.expr2.toString()
