import copy
from libs.parsers.data import Data
from libs.parsers.first import First

class Generator:
    def __init__(self, data: Data, first_set: First):
        self.sta_set = {}
        self.sta_table = {}
        self.action = {}
        self.goto = {}
        self.first = first_set
        self.data = data
        self.set_status = self.__set_sta_set()
        self.aniz_status = self.__set_aniz_table()

    def __closure(self, ele: set) -> set:
        '''
        计算集合闭包
        '''
        res = set()
        res.update(ele)
        # print(res)
        flag = 1
        res_t: set = copy.deepcopy(res)
        while flag == 1:
            flag = 0
            res_p = set()
            for i in res_t:
                R_pp: str = i[0]
                R_str: tuple = copy.deepcopy(i[1])
                R_nxt: tuple = copy.deepcopy(i[2])
                point_pos = R_str.index('·')
                length = len(R_str)
                if point_pos+1 < length and R_str[point_pos+1] in self.data.noend:
                    # 点后有字符且字符为非终结符
                    for j in self.data.grammar_item:
                        if j[0] == R_str[point_pos+1]:
                            # 文法的归约项目为点后第一个非终结符
                            head: str = j[0]
                            new: list = copy.deepcopy(j[1])
                            new.insert(0, '·')
                            if 'ε' in new:
                                new.remove('ε')
                            nxt = set()
                            if point_pos+2 < length:
                                # 点后两位有字符
                                for l in R_nxt:
                                    s = copy.deepcopy(R_str[point_pos+2:])
                                    s = list(s)
                                    s.append(l)
                                    nxt.update(self.first.get_first(s))
                            else:
                                # 点后两位无字符，则复制nxt集
                                nxt = copy.deepcopy(R_nxt)
                            # 确认nxt的顺序
                            nxt = list(nxt)
                            nxt.sort()
                            ans = (head, tuple(new), tuple(nxt))
                            if ans not in res:
                                res_p.add(ans)
                                flag = 1
            res_t = copy.deepcopy(res_p)
            res.update(res_p)
        # 合并闭包中的相同条目
        res = self.__merge(res)
        return res

    def __merge(self, s: set) -> set:
        res = set()
        pool = set()
        res_t = list(s)
        for i in range(len(res_t)):
            x = (res_t[i][0], res_t[i][1])
            if x in pool:
                continue
            pt = set()
            for j in range(i+1, len(res_t)):
                if res_t[i][0] == res_t[j][0] and res_t[i][1] == res_t[j][1]:
                    pt.update(set(res_t[j][2]))
            pt.update(set(res_t[i][2]))
            pool.add(x)
            # 确认pt(nxt)的顺序
            pt = list(pt)
            pt.sort()
            res.add((res_t[i][0], res_t[i][1], tuple(pt)))
        return res

    def __set_sta_set(self) -> bool:
        '''
        构造项目集规范族
        '''
        st = (self.data.grammar_item[0][0], ('·',) +
              tuple(self.data.grammar_item[0][1]), ('#',))
        st_set = set()
        st_set.add(st)
        I = self.__closure(st_set)
        index = 0
        self.sta_set[index] = I
        self.sta_table[index] = {}
        pool = set()
        I_now = set()
        index += 1
        index_search = 0
        while index_search < len(self.sta_set):
            pool.clear()
            I_now.clear()
            for i in self.sta_set[index_search]:
                i = list(i)
                point_pos = i[1].index('·')
                if point_pos+1 < len(i[1]):
                    point_pos += 1
                    x = i[1][point_pos]
                    if x not in pool:
                        pool.add(x)
                        I_now = self.__get_same(index_search, x)
                        # print('\033[1;31m构造集合\033[0m',I_now)
                        I = self.__closure(I_now)
                        if I not in self.sta_set.values():
                            self.sta_table[index_search][x] = index
                            self.sta_set[index] = I
                            self.sta_table[index] = {}
                            index += 1
                            # print('\033[1;32mTrue\033[0m',index-1)
                        else:
                            ind = list(self.sta_set.keys())[
                                list(self.sta_set.values()).index(I)]
                            self.sta_table[index_search][x] = ind
                            # print('\033[1;31mFalse\033[0m')
            index_search += 1
        return True

    def __get_same(self, index: int, st: str) -> set:
        '''
        获取集合中相同'·'后字符的集合
        '''
        # sta_set内结构：1:{('S',('·','a'),('#',))}
        res = set()
        for i in self.sta_set[index]:
            i = list(i)
            point_pos = i[1].index('·')
            if point_pos+1 < len(i[1]) and i[1][point_pos+1] == st:
                new = copy.deepcopy(i[1])
                new = list(new)
                new.remove('·')
                new.insert(point_pos+1, '·')
                new = tuple(new)
                res.add((i[0], new, i[2]))
        return res

    def __set_aniz_table(self) -> bool:
        '''
        构造LR(1)分析表
        '''
        for i, j in self.sta_set.items():
            self.action[i] = {}
            for end in self.data.end:
                self.action[i][end] = None
            self.action[i]['#'] = None
            self.goto[i] = {}
            for noend in self.data.noend:
                self.goto[i][noend] = None
            self.goto[i].pop("S'")
            for k in j:
                if k[1][-1] == '·':
                    t = list(k[1])
                    t.remove('·')
                    if t == []:
                        t.append('ε')
                    x = (k[0], t)
                    pos = self.data.grammar_item.index(x)
                    for l in k[2]:
                        if k[0] == "S'":
                            self.action[i][l] = 'acc'
                        else:
                            self.action[i][l] = 'R'+'{}'.format(pos)
            for k, l in self.sta_table[i].items():
                if k in self.data.end:
                    self.action[i][k] = 'S'+'{}'.format(l)
                else:
                    self.goto[i][k] = l
        return True