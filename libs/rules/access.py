from libs.rules.op import Op
from libs.symbols.type import Type
from libs.lexers.word import Word
from libs.lexers.tag import Tag


class Access(Op):
    def __init__(self, a, i, p):
        super(Access, self).__init__(Word('[]', Tag.INDEX), p)
        self.array = a
        self.index = i

    def gen(self):
        return Access(self.array, self.index.reduce(), self.type)

    def jumping(self, t, f):
        self.emitjumps(self.reduce().toString(), t, f)

    def toString(self):
        return self.array.toString()+' [ '+self.index.toString()+' ] '
