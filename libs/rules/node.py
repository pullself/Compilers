from libs.lexers.lexer import Lexer


class Node():
    labels = 0

    def __init__(self, no: int = 0):
        self.lexline = Lexer.line[no]

    def new_label(self):
        Node.labels += 1
        return Node.labels

    def emit_label(self, i):
        f = open('Intermediate_Language.txt','a')
        print('L'+str(i)+':', end='',file=f)
        f.close()

    def emit(self, s):
        f = open('Intermediate_Language.txt','a')
        print('\t'+s,file=f)
        f.close()

    def error(self, s):
        raise RuntimeError('near line '+str(self.lexline)+': '+s)
