class Env:
    def __init__(self, pre=None):
        self.table = {}
        self.pre = pre

    def put(self, w, i):
        self.table.update({w: i})

    def get(self, w):
        e = self
        while e:
            found = e.table.get(w)
            if found:
                return found
            e = e.pre
        return None
