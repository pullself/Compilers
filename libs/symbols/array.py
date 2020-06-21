from libs.symbols.type import Type
from libs.lexers.tag import Tag


class Array(Type):
    def __init__(self, sz: int, p: Type):
        # sz 是数组长度
        # p 是数组类型
        super(Array, self).__init__('[]', Tag.INDEX, sz*p.width)
        self.size = sz
        self.of = p

    def toString(self):
        return '['+self.size+']'+self.of.toString()
