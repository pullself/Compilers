import argparse
from libs.parsers.constructor import Constructor
from libs.lexers.lexer import Lexer
from libs.lexers.tag import Tag
from libs.parsers.parser import Parser

class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.argInit()
        if self.parser.parse_args().construct:
            self.construct(self.parser.parse_args().construct)
        elif self.parser.parse_args().analyze:
            self.analyze(self.parser.parse_args().analyze)

    def argInit(self):
        self.parser.add_argument('-c','--construct',help='构造分析表，输入文法文件地址')
        self.parser.add_argument('-a','--analyze',help='执行分析，输入代码文件地址')
        
    def construct(self,addr):
        g = Constructor(addr)
        g.output()

    def analyze(self,addr):
        with open(addr, 'r') as f:
            s = f.readlines()
        le = Lexer(s)
        gr = Parser('action.json','goto.json','grammar.json',le)
        gr.scan()

if __name__ == '__main__':
    main = Main()



