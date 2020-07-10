import collections
from libs.lexers.tag import Tag,Key
from libs.lexers.token import Token
from libs.lexers.num import Num
from libs.lexers.real import Real
from libs.lexers.word import Word, Words
from libs.symbols.type import Types


class Lexer:
    # 保留字表
    key = {'if': Word('if', Tag.IF), 'else': Word('else', Tag.ELSE),
           'while': Word('while', Tag.WHILE), 'do': Word('do', Tag.DO),
           'break': Word('break', Tag.BREAK), 'int': Types.Int,
           'float': Types.Float, 'char': Types.Char,
           'bool': Types.Bool, 'true': Words.true,
           'false': Words.false}
    # 界符表
    delimiter = ['{', '}', '[', ']', '(', ')',  ';']
    # 各表对应偏移量常量
    key_num = 1
    delimiter_num = 15
    line = [1]

    def __init__(self, resorce: list):
        self.__resource_project = resorce
        self.__cache = ''
        # self.__token = ''
        self.__p = 0
        self.__ch = None
        self.no = len(Lexer.line)-1
        Lexer.line.append(1)
        # 词法符号表
        self.wordtable = {}
        # 自动机注册字典
        self.__sta = {
            0: self.__start,
            1: self.__id_check_1,
            2: self.__id_check_2,
            3: self.__num_check_1,
            4: self.__int_check,
            5: self.__real_check_1,
            6: self.__real_check_2,
            7: self.__E_check_1,
            8: self.__E_check_2,
            9: self.__E_check_3,
            10: self.__E_check_4,
            20: self.__delimit,
            22: self.__bitwise_2,
            24: self.__logic,
            25: self.__arith_com_1,
            26: self.__arith_com_2,
            27: self.__arith_ass_com,
            100: self.__end
        }
        self.__resource_filter()

    def __resource_filter(self):
        '''
        预处理
        '''
        # project_interim = self.__resource_project.replace('\n', '')
        # project_interim = ' '.join(project_interim.split())
        # project_interim += '#'
        # self.__resource_project = project_interim
        # self.__ch = self.__nextchar()
        # --------------------------------------
        for i in range(len(self.__resource_project)):
            self.__resource_project[i] = self.__resource_project[i].replace(
                '\n', '')
            self.__resource_project[i] = ' '.join(
                self.__resource_project[i].split())
        self.__resource_project = list(
            filter(lambda x: len(x) != 0, self.__resource_project))
        self.__resource_project[-1] += '#'
        self.__ch = self.__nextchar()

    def __nextchar(self) -> str:
        '''
        取下一字符
        '''
        c = self.__resource_project[Lexer.line[self.no]-1][self.__p]
        self.__p += 1
        if self.__p == len(self.__resource_project[Lexer.line[self.no]-1]):
            Lexer.line[self.no] += 1
            self.__p = 0
        return c

    def __is_letter(self, letter: str) -> bool:
        '''
        判断是否为字母
        '''
        return letter.isalpha()

    def __is_digit(self, digit: str) -> bool:
        '''
        判断是否为数字
        '''
        return digit.isdigit()

    def __is_key(self, key: str) -> bool:
        '''
        判断是否为保留字
        '''
        if key in self.key.keys():
            return key
        else:
            return False

    def __start(self):
        if self.__ch == ' ':
            self.__ch = self.__nextchar()
            return self.__sta.get(0)()
        elif self.__is_letter(self.__ch) or self.__ch == '_':
            self.__cache += self.__ch
            return self.__sta.get(1)()
        elif self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(3)()
        elif self.__ch in self.delimiter:
            return self.__sta.get(20)()
        elif self.__ch == '&' or self.__ch == '|':
            self.__cache += self.__ch
            return self.__sta.get(22)()
        elif self.__ch == '=' or self.__ch == '+' or self.__ch == '-' or self.__ch == '*' or self.__ch == '/' or self.__ch == '!' or self.__ch == '<' or self.__ch == '>':
            self.__cache += self.__ch
            return self.__sta.get(25)()
        elif self.__ch == '#':
            return self.__sta.get(100)()
        else:
            return self.__fail()
            self.__ch = self.__nextchar()

    def __id_check_1(self):
        self.__ch = self.__nextchar()
        if self.__is_digit(self.__ch) or self.__is_letter(
                self.__ch) or self.__ch == '_':
            self.__cache += self.__ch
            return self.__sta.get(1)()
        else:
            return self.__sta.get(2)()

    def __id_check_2(self):
        res = self.__is_key(self.__cache)
        if res is not False:
            return self.key[res]
        else:
            if self.__cache not in self.wordtable.keys():
                new = Word(self.__cache, Tag.ID)
                self.wordtable.update({self.__cache: new})
                return new
            else:
                return self.wordtable.get(self.__cache)

    def __num_check_1(self):
        self.__ch = self.__nextchar()
        if self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(3)()
        elif self.__ch == '.':
            self.__cache += self.__ch
            return self.__sta.get(5)()
        elif self.__ch == 'E' or self.__ch == 'e':
            self.__cache += self.__ch
            return self.__sta.get(7)()
        else:
            return self.__sta.get(4)()

    def __int_check(self):
        return Num(int(self.__cache))

    def __real_check_1(self):
        self.__ch = self.__nextchar()
        if self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(5)()
        elif self.__ch == 'E' or self.__ch == 'e':
            self.__cache += self.__ch
            return self.__sta.get(7)()
        else:
            return self.__sta.get(6)()

    def __real_check_2(self):
        return Real(float(self.__cache))

    def __E_check_1(self, tag):
        self.__ch = self.__nextchar()
        if self.__ch == '+' or self.__ch == '-':
            self.__cache += self.__ch
            return self.__sta.get(8)()
        elif self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(9)()

    def __E_check_2(self, tag):
        self.__ch = self.__nextchar()
        if self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(9)()
        else:
            return self.__fail()

    def __E_check_3(self, tag):
        self.__ch = self.__nextchar()
        if self.__is_digit(self.__ch):
            self.__cache += self.__ch
            return self.__sta.get(9)()
        else:
            return self.__sta.get(10)()

    def __E_check_4(self):
        return Real(eval(self.__cache))

    def __delimit(self):
        res = self.delimiter.index(self.__ch)
        self.__ch = self.__nextchar()
        return Token(Tag(res + self.delimiter_num))

    def __bitwise_2(self):
        self.__ch = self.__nextchar()
        if self.__ch == self.__cache:
            self.__cache += self.__ch
            return self.__sta.get(24)()
        elif self.__ch == ' ':
            return self.__sta.get(22)()
        else:
            return self.__fail()

    def __logic(self):
        self.__ch = self.__nextchar()
        if self.__cache == '&&':
            return Words.And
        else:
            return Words.Or

    def __arith_com_1(self):
        self.__ch = self.__nextchar()
        if self.__ch == '=':
            self.__cache += self.__ch
            return self.__sta.get(27)()
        elif self.__ch == ' ':
            return self.__sta.get(25)()
        else:
            return self.__sta.get(26)()

    def __arith_com_2(self):
        if self.__cache == '+':
            return Token(Tag.ADDITIONOPERATOR)
        elif self.__cache == '-':
            return Token(Tag.SUBTRACTIONOPERATOR)
        elif self.__cache == '*':
            return Token(Tag.MULTIPLICATIONOPERATOR)
        elif self.__cache == '/':
            return Token(Tag.DIVISIONOPERATOR)
        elif self.__cache == '!':
            return Token(Tag.LOGICNOT)
        elif self.__cache == '<':
            return Token(Tag.LESS)
        elif self.__cache == '=':
            return Token(Tag.ASSIGNMENTOPERATOR)
        else:
            return Token(Tag.GREATER)

    def __arith_ass_com(self):
        self.__ch = self.__nextchar()
        if self.__cache == '!=':
            return Words.Ne
        elif self.__cache == '<=':
            return Words.le
        elif self.__cache == '==':
            return Words.Eq
        elif self.__cache == '>=':
            return Words.Ge
        else:
            return self.__fail()

    def __end(self):
        return Token(Tag.END)

    def __fail(self):
        return Token(Tag.ERROR)

    def __scanner(self):
        '''
        扫描入口
        '''
        self.__cache = ''
        return self.__sta.get(0)()

    def get_line(self):
        return Lexer.line[self.no]

    def get_next_word(self):
        '''
        取词接口
        '''
        return self.__scanner()

    def get_word_unit(self) -> tuple:
        word_unit = collections.namedtuple('word_unit', ['tag', 'value'])
        x = self.get_next_word()
        tag = x.tag
        if isinstance(x, Num) or isinstance(x, Real):
            value = x.value
        elif x.tag == Tag.BASIC or x.tag == Tag.ID:
            value = x.lexeme
        else:
            value = None
        obj = word_unit(tag, value)
        return obj
