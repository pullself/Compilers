from libs.rules.stmt import Stmt, Stmts


class Break(Stmt):
    loop_flag = []
    break_list = []
    def __init__(self):
        super(Break, self).__init__()
        # if Stmts.Enclosing == Stmts.Null:
        #     self.error('unenclosed break')
        # self.stmt = Stmts.Enclosing
        if not Break.loop_flag:
            self.error('unenclosed break')
        self.stmt = None
        Break.break_list.append(self)

    def gen(self, b, a):
        self.emit('goto L'+str(self.stmt.after))
