from libs.rules.stmt import Stmt
from libs.rules.access import Access
from libs.symbols.array import Array
from libs.symbols.type import Type, Types
from libs.lexers.num import Num


class SetElem(Stmt):
    def __init__(self, x: Access, y):
        super(SetElem, self).__init__()
        self.array = x.array
        self.index = x.index
        self.expr = y
        if self.check(x.type, self.expr.type) == None:
            self.error('type error')

    def check(self, p1, p2):
        if isinstance(p1, Array) or isinstance(p2, Array):
            return None
        elif p1 == p2:
            return p2
        elif Type.numeric(p1) and Type.numeric(p2):
            return p2
        else:
            return None

    def gen(self, b, a):
        if isinstance(self.index,Num):
            s1 = self.index.toString()
        else:
            # 允许索引为表达式的时候使用
            s1 = self.index.reduce().toString()
        s2 = self.expr.reduce().toString()
        self.emit(self.array.toString()+' [ '+s1+' ] = '+s2)
