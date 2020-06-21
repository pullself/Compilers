from libs.lexers.token import Token
from libs.lexers.tag import Tag


class Word(Token):
    def __init__(self, s: str, tag: int):
        super(Word, self).__init__(tag)
        self.lexeme = s

    def toString(self) -> str:
        return self.lexeme


class Words():
    And = Word('&&', Tag.LOGICAND,)
    Or = Word('||', Tag.LOGICOR)
    Eq = Word('==', Tag.EQUALOPERATOR)
    Ne = Word('!=', Tag.NOTEQUALOPERATOR,)
    Le = Word('<=', Tag.LESSEQUAL)
    Ge = Word('>=', Tag.GREATEREQUAL)
    true = Word('true', Tag.TRUE)
    false = Word('false', Tag.FALSE)
    temp = Word('temp', Tag.TEMP)
    minus = Word('minus',Tag.MINUS)
    count = 10
