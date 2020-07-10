import argparse
from libs.parsers.constructor import Constructor
from libs.lexers.lexer import Lexer
from libs.lexers.tag import Tag, Key
from libs.parsers.parser import Parser
from libs.statistic import Drawer

class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.argInit()
        if self.parser.parse_args().construct:
            self.construct(self.parser.parse_args().construct)
        elif self.parser.parse_args().analyze:
            self.analyze(self.parser.parse_args().analyze)
        elif self.parser.parse_args().lexer:
            self.lexer(self.parser.parse_args().lexer)

    def argInit(self):
        self.parser.add_argument('-l', '--lexer', help='输出词法表')
        self.parser.add_argument('-c', '--construct', help='构造分析表，输入文法文件地址')
        self.parser.add_argument('-a', '--analyze', help='执行分析，输入代码文件地址')

    def construct(self, addr):
        g = Constructor(addr)
        g.output()
        first_set,generater = g.get_pic()
        Drawer.trans('action.json','goto.json', 'my.csv','w')
        Drawer.write_first(first_set.first_set)
        Drawer.write_sta_set(generater.sta_set,generater.sta_table)

    def analyze(self, addr):
        with open(addr, 'r') as f:
            s = f.readlines()
        le = Lexer(s)
        gr = Parser('action.json', 'goto.json', 'grammar.json', le)
        gr.scan()

    def lexer(self, addr):
        with open(addr, 'r',encoding = 'utf-8') as f:
            s = f.readlines()
        le = Lexer(s)
        x = le.get_word_unit()
        tag = []
        value = []
        while x.tag != Tag.END:
            tag.append(Key[x.tag])
            value.append(str(x.value))
            x = le.get_word_unit()
        tag.append(Key[x.tag])
        value.append(str(x.value))
        Drawer.change_output_lexer(tag,value)



if __name__ == '__main__':
    main = Main()
