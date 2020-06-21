from libs.lexers.tag import Key


class Token:
    def __init__(self, t):
        self.tag = t

    def toString(self) -> str:
        return Key[self.tag]
