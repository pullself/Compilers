from libs.rules.node import Node

class Stmt(Node):
    def __init__(self):
        super(Stmt,self).__init__()
        self.after = 0

    def gen(self,b,a):
        pass

class Stmts:
    Null = Stmt()
    Enclosing = Null