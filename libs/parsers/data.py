class Data:
    def __init__(self, grammar: list):
        self.end = set()
        self.noend = set()
        self.grammar_item = None
        self.initialize(grammar)

    def initialize(self, grammar):
        '''
        文法处理
        '''
        res = [("S'", [grammar[0].split('->')[0]])]
        for i in grammar:
            i = ' '.join(i.split())
            res += self.__cut(i)
        for i in res:
            self.noend.add(i[0])
            self.end = self.end.union({j for j in i[1]})
        self.end = {i for i in self.end if i not in self.noend}
        if 'ε' in self.end:
            self.end.remove('ε')
        self.grammar_item = tuple(res)

    def __cut(self, s: str) -> list:
        res = []
        pa = s.split('->')
        left = pa[0]
        if '||' in pa[1]:
            pa[1] = pa[1].replace('||', '$')
        right = pa[1].split('|')
        for i in range(len(right)):
            if '$' in right[i]:
                right[i] = right[i].replace('$', '||')
        for i in range(len(right)):
            res.append((left, right[i].split(' ')))
        return res
