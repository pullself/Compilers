import json
from libs.parsers.data import Data
from libs.parsers.first import First
from libs.parsers.generator import Generator


class Constructor:
    def __init__(self, addr: str):
        with open(addr, 'r', encoding='utf-8') as f:
            self.gra = f.readlines()
            for i in range(len(self.gra)):
                self.gra[i] = self.gra[i].replace('\n', '')
        self.__init_data = Data(self.gra)
        self.__first = First(self.__init_data)
        self.__generater = Generator(self.__init_data, self.__first)

    def output(self):
        with open('grammar.json', 'w', encoding='utf-8') as f:
            json.dump(self.__init_data.grammar_item, f, ensure_ascii=False)
        with open('action.json', 'w', encoding='UTF-8') as f:
            json.dump(self.__generater.action, f, ensure_ascii=False)
        with open('goto.json', 'w', encoding='UTF-8') as f:
            json.dump(self.__generater.goto, f, ensure_ascii=False)
