import prettytable as pt
import copy


class Table:
    def __init__(self):
        self.table = pt.PrettyTable()
        self.labels = 1

    def add_field(self, li):
        self.table.field_names = li
        for i in self.table.align.keys():
            self.table.align[i] = 'l'

    def add_row(self, li):
        data = copy.deepcopy(li)
        self.table.add_row([self.labels]+data)
        self.labels += 1

    def show(self):
        print(self.table)
