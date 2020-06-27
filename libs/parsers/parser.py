import json
import time
import sys
from libs.lexers.lexer import Lexer
from libs.lexers.token import Token
from libs.lexers.tag import Tag, Key
from libs.lexers.num import Num
from libs.lexers.word import Word, Words
from libs.symbols.type import Type, Types
from libs.symbols.array import Array
from libs.symbols.env import Env
from libs.rules.constant import Constant, Constants
from libs.rules.id import Id
from libs.rules.access import Access
from libs.rules.arith import Arith
from libs.rules._and import And
from libs.rules._or import Or
from libs.rules.rel import Rel
from libs.rules._not import Not
from libs.rules.unary import Unary
from libs.rules.stmt import Stmts
from libs.rules._if import If
from libs.rules._else import Else
from libs.rules._while import Whlie
from libs.rules.do import Do
from libs.rules._break import Break
from libs.rules.set import Set
from libs.rules.setelem import SetElem
from libs.rules.seq import Seq
from libs.statistic.visualization import Table


class Parser:
    def __init__(self, ac_addr: str = None, goto_addr: str = None, grammar_addr: str = None, lex: Lexer = None):
        self.__key = Key
        self.__nxt_word = None
        self.__lexer = lex
        self.__sta_stack = ['0']
        self.__word_stack = ['#']
        self.__value_stack = [None]
        self.__action = None
        self.__goto = None
        self.__gra = None
        self.look: Token = None
        self.top: Env = None
        self.cache = []
        self.used = 0
        self.env_flag = 0
        self.set_action(ac_addr)
        self.set_goto(goto_addr)
        self.set_grammar(grammar_addr)
        self.output = Table()
        self.output.add_field(['序号', '状态栈', '符号栈', '当前字符', '动作'])
        f = open('Intermediate_Language.txt', "w+")
        f.close()

    def __get_nxt_word(self) -> str:
        self.look = self.__lexer.get_next_word()
        return self.look

    def set_lexer(self, le: Lexer):
        self.__lexer = le

    def set_action(self, ac_addr: str):
        if ac_addr is not None:
            with open(ac_addr, 'r', encoding='utf-8') as f:
                self.__action = json.load(f)
        else:
            self.__action = None

    def set_goto(self, goto_addr: str):
        if goto_addr is not None:
            with open(goto_addr, 'r', encoding='utf-8') as f:
                self.__goto = json.load(f)
        else:
            self.__goto = None

    def set_grammar(self, gra_addr: str):
        if gra_addr is not None:
            with open(gra_addr, 'r', encoding='utf-8') as f:
                self.__gra = json.load(f)
        else:
            self.__gra = None

    def __error(self, s, offset=0):
        self.output.show()
        raise RuntimeError('near line {}:'.format(
            self.__lexer.get_line()-offset)+s)

    def scan(self):
        wd: Token = self.__get_nxt_word()
        if wd.tag == Tag.ERROR:
            self.__error('Invalid Word: {}'.format(wd.tag))
        else:
            wd_ori = self.__key[wd.tag]
        while 1:
            ac = self.__action[self.__sta_stack[-1]][wd_ori]
            if ac == 'acc':
                self.output.show()
                return 'Finish'
            elif ac is None:
                self.__error('Invalid Syntax')
            elif ac[0] == 'S':
                self.__word_stack.append(wd_ori)
                self.__sta_stack.append(ac[1:])
                self.__value_stack.append(wd)
                if wd_ori == 'while' or wd_ori == 'do':
                    Break.loop_flag.append(len(Break.break_list))
                # print(self.__sta_stack, self.__word_stack)
                self.output.add_row(
                    [self.__sta_stack, self.__word_stack, wd_ori, '移入'])
                # print(self.__value_stack)
                wd = self.__get_nxt_word()
                if wd.tag == Tag.ERROR:
                    self.__error('Invalid Word: {}'.format(wd.tag))
                else:
                    wd_ori = self.__key[wd.tag]
            elif ac[0] == 'R':
                num = int(ac[1:])
                r = self.__gra[num]
                self.cache.clear()
                if 'ε' not in r[1]:
                    for i in range(len(r[1])):
                        self.__sta_stack.pop()
                        self.__word_stack.pop()
                        x = self.__value_stack.pop()
                        self.cache.append(x)
                self.__word_stack.append(r[0])
                self.__sta_stack.append(
                    str(self.__goto[self.__sta_stack[-1]][r[0]]))
                self.cache.reverse()
                if num == 1:
                    # program
                    self.__program()
                elif num == 2:
                    # block
                    self.__block()
                elif num == 3 or num == 4:
                    # decls
                    self.__decls()
                elif num == 5:
                    # decl
                    self.__decl()
                elif num == 6 or num == 7:
                    # type
                    self.__type(num)
                elif num == 8 or num == 9:
                    # stmts
                    self.__stmts(num)
                elif num == 10 or num == 11 or num == 12 or num == 13 or num == 14 or num == 15 or num == 16:
                    # stmt
                    self.__stmt(num)
                elif num == 17 or num == 18:
                    # loc
                    self.__loc(num)
                elif num == 19 or num == 20:
                    # bool
                    self.__bool(num)
                elif num == 21 or num == 22:
                    # join
                    self.__join(num)
                elif num == 23 or num == 24 or num == 25:
                    # equality
                    self.__equality(num)
                elif num == 26 or num == 27 or num == 28 or num == 29 or num == 30:
                    # rel
                    self.__rel(num)
                elif num == 31 or num == 32 or num == 33:
                    # expr
                    self.__expr(num)
                elif num == 34 or num == 35 or num == 36:
                    # term
                    self.__term(num)
                elif num == 37 or num == 38 or num == 39:
                    # unary
                    self.__unary(num)
                else:
                    # factor
                    self.__factor(num)
                # print(self.__sta_stack, self.__word_stack)
                s = '归约' + r[0] + '->'
                for i in r[1]:
                    s += i
                self.output.add_row(
                    [self.__sta_stack, self.__word_stack, wd_ori, s])
                # print(self.__value_stack)

    def __program(self):
        s: Seq = self.cache[0]
        begin = s.new_label()
        after = s.new_label()
        s.emit_label(begin)
        s.gen(begin, after)
        s.emit_label(after)
        self.__value_stack.append(None)

    def __block(self):
        # 返回上一级的变量域
        self.top = self.top.pre
        # 保存stmts语句
        self.__value_stack.append(self.cache[2])

    def __decls(self):
        if self.env_flag == 0:
            # 标记位为0时，进入新的变量域，生成新的符号表
            self.env_flag = 1
            self.top = Env(self.top)
        # 定义语句不需要定义语法树
        self.__value_stack.append(None)

    def __decl(self):
        if self.env_flag == 0:
            # 标记位为0时，进入新的变量域，生成新的符号表
            self.env_flag = 1
            self.top = Env(self.top)
        # 将标识符存进对应的符号表
        tok = self.cache[1]
        p = self.cache[0]
        _id = Id(tok, p, self.used)  # 生成新的标识符对象
        self.top.put(tok, _id)
        self.used += p.width  # 内存分配
        self.__value_stack.append(None)

    def __type(self, num):
        # 归约为Type类型
        if num == 6:
            # 数组类型（Array）
            arr = Array(self.cache[2].value, self.cache[0])
            self.__value_stack.append(arr)
        else:
            # 基础类型basic（Type）
            self.__value_stack.append(self.cache[0])

    def __stmts(self, num):
        if self.env_flag == 1:
            # 变量域定义结束
            self.env_flag = 0
            # for i, j in self.top.table.items():
            #     print(i.lexeme, j.type.tag, j.offset)
        if num == 8:
            # 处理语句集
            stmts = self.cache[0]
            stmts_temp = stmts
            stmt = self.cache[1]
            if isinstance(stmts_temp, Seq):
                while isinstance(stmts_temp.stmt2, Seq):
                    stmts_temp = stmts_temp.stmt2
                seq_temp = Seq(stmts_temp.stmt2, stmt)
                stmts_temp.stmt2 = seq_temp
                x = stmts
            else:
                x = Seq(stmts, stmt)
        else:
            # 空语句
            x = Stmts.Null
        self.__value_stack.append(x)

    def __stmt(self, num):
        if num == 10:
            # 赋值语句
            left = self.cache[0]
            right = self.cache[2]
            # 非数组判断
            if isinstance(left, Id) and left.type.tag == Tag.INDEX:
                self.__error(left.toString()+' is an array')
            if isinstance(left, Id):
                # 左部为标识符
                x = Set(left, right)
            else:
                # 左部为数组
                x = SetElem(left, right)
        elif num == 11:
            # if语句
            cond = self.cache[2]
            stmt = self.cache[4]
            x = If(cond, stmt)
        elif num == 12:
            # if/else语句，就近匹配原则
            cond = self.cache[2]
            stmt1 = self.cache[4]
            stmt2 = self.cache[6]
            x = Else(cond, stmt1, stmt2)
        elif num == 13:
            # while语句
            cond = self.cache[2]
            stmt = self.cache[4]
            x = Whlie()
            for i in range(Break.loop_flag[-1], len(Break.break_list)):
                Break.break_list[i].stmt = x
            Break.loop_flag.pop()
            x.init(cond, stmt)
        elif num == 14:
            # do语句
            stmt = self.cache[1]
            cond = self.cache[4]
            x = Do()
            Break.loop_flag.pop()
            for i in range(Break.loop_flag[-1], len(Break.break_list)):
                Break.break_list[i].stmt = x
            Break.loop_flag.pop()
            x.init(stmt, cond)
        elif num == 15:
            # break语句
            x = Break()
        else:
            x = self.cache[0]
        self.__value_stack.append(x)

    def __loc(self, num):
        if num == 17:
            # 数组归约
            _id = self.cache[0]
            # 数组判断
            if _id.type.tag != Tag.INDEX:
                self.__error(_id.toString()+' is not an array')
            access = self.__offset(_id)
            self.__value_stack.append(access)
        else:
            # 单一变量归约，非数组判断在stmt解决
            _id = self.top.get(self.cache[0])
            # 判断是否定义
            if _id == None:
                self.__error(self.cache[0].toString()+' undeclared')
            self.__value_stack.append(_id)

    def __bool(self, num):
        if num == 19:
            x = Or(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __join(self, num):
        if num == 21:
            x = And(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __equality(self, num):
        if num == 23 or num == 24:
            x = Rel(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __rel(self, num):
        if num == 26 or num == 27 or num == 28 or num == 29:
            x = Rel(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __expr(self, num):
        if num == 31 or num == 32:
            x = Arith(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __term(self, num):
        if num == 34 or num == 35:
            x = Arith(self.cache[1], self.cache[0], self.cache[2])
            self.__value_stack.append(x)
        else:
            self.__value_stack.append(self.cache[0])

    def __unary(self, num):
        if num == 37:
            x = Not(self.cache[0], self.cache[1])
        elif num == 38:
            x = Unary(Token(Tag.MINUS), self.cache[1])
        else:
            x = self.cache[0]
        self.__value_stack.append(x)

    def __factor(self, num):
        x = None
        if num == 40:
            # (bool)
            x = self.cache[1]
        elif num == 41:
            # loc
            x = self.cache[0]
        elif num == 42:
            # 整型
            x = Constant(self.cache[0], Types.Int)
        elif num == 43:
            # 实型
            x = Constant(self.cache[0], Types.Float)
        elif num == 44:
            # 布尔真
            x = Constants.true
        elif num == 45:
            # 布尔假
            x = Constants.false
        self.__value_stack.append(x)

    def __offset(self, a):
        # 处理数组
        if isinstance(a, Access):
            # 多维数组
            _type = a.type.of
            w = Constant(_type.width)
            i = self.cache[2]
            t1 = Arith(Token(Tag.MULTIPLICATIONOPERATOR), i, w)
            t2 = Arith(Token(Tag.ADDITIONOPERATOR), a.index, t1)
            access = Access(a.array, t2, _type)
            # # 判断越界（编译时无法实现）
            # if self.cache[2].value >= a.type.size:
            #     self.__error(a.toString()+' out of range')
        else:
            _type = a.type.of
            w = Constant(_type.width)
            i = self.cache[2]
            t1 = Arith(Token(Tag.MULTIPLICATIONOPERATOR), i, w)
            access = Access(a, t1, _type)
            # # 判断越界（编译时无法实现）
            # if self.cache[2].value >= a.type.size:
            #     self.__error(a.toString()+' out of range')
        return access
