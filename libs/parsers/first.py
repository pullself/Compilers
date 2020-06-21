import copy
from libs.parsers.data import Data


class First:
    def __init__(self, data: Data):
        self.first_set = {}
        self.count = 0
        self.end = data.end
        self.noend = data.noend
        self.status = self.set_first(data.grammar_item)

    def set_first(self, grammar_item) -> bool:
        '''
        构建非终结符First集。\n
        True代表构建成功，False代表构建失败
        '''
        for i in self.noend:
            self.first_set.update({i: set()})
        self.count = len(self.noend)
        flag = 1
        while flag == 1:
            flag = 0
            for i in grammar_item:
                j = 0
                while 1:
                    if j == len(i[1]):
                        self.first_set[i[0]].add('ε')
                        flag = 1
                        break
                    elif i[1][j] in self.end or i[1][j] == 'ε':
                        if i[1][j] not in self.first_set[i[0]]:
                            self.first_set[i[0]].add(i[1][j])
                            flag = 1
                        break
                    elif i[1][j] in self.noend:
                        if 'ε' in self.first_set[i[1][j]]:
                            fir_son: set = copy.deepcopy(
                                self.first_set[i[1][j]])
                            fir_son.remove('ε')
                            p = self.first_set[i[0]].intersection(fir_son)
                            if p != fir_son:
                                self.first_set[i[0]].update(fir_son)
                                flag = 1
                            j += 1
                            continue
                        else:
                            fir_son = copy.deepcopy(self.first_set[i[1][j]])
                            p = self.first_set[i[0]].intersection(fir_son)
                            if p != fir_son:
                                self.first_set[i[0]].update(fir_son)
                                flag = 1
                            break
                    else:
                        return False
        return True

    def get_first(self, ele: list) -> set:
        '''
        获取串的First集。
        '''
        res = set()
        for i in ele:
            if i in self.end or i == 'ε' or i == '#':
                res.add(i)
                return res
            elif i in self.noend:
                if 'ε' in self.first_set[i]:
                    res.update(self.first_set[i])
                    res.remove('ε')
                else:
                    res.update(self.first_set[i])
                    return res
            else:
                return set()
        if not res:
            res.add('ε')
        return res
