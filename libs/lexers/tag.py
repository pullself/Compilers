from enum import Enum


class Tag(Enum):
    END = 0
    PROGRAM = 1
    IF = 2  # if
    ELSE = 3  # else
    WHILE = 4  # while
    DO = 5  # do
    BREAK = 6  # break
    TRUE = 11  # true
    FALSE = 12  # false
    BASIC = 14  # basic
    LEFTBRACE = 15  # {
    RIGHTBRACE = 16  # }
    LEFTBRACKETS = 17  # [
    RIGHTBRACKETS = 18  # ]
    LEFTPARENTHESE = 19  # (
    RIGHTPARENTHESE = 20  # )
    SEMICOLON = 21  # ;
    ASSIGNMENTOPERATOR = 40  # =
    ADDITIONOPERATOR = 41  # +
    SUBTRACTIONOPERATOR = 42  # -
    MULTIPLICATIONOPERATOR = 43  # '*'
    DIVISIONOPERATOR = 44  # /
    ADDITIONASSOPERATOR = 45
    SUBTRACTIONASSOPERATOR = 46
    MULTIPLICATIONASSOPERATOR = 47
    DIVISIONASSOPERATOR = 48
    LOGICNOT = 49  # '!'
    EQUALOPERATOR = 50  # ==
    NOTEQUALOPERATOR = 51  # '!='
    GREATER = 52  # >
    LESS = 53  # <
    GREATEREQUAL = 54  # >=
    LESSEQUAL = 55  # <=
    LOGICAND = 60  # &&
    LOGICOR = 61  # ||
    ID = 100  # id
    NUM = 101  # num
    REAL = 102  # real
    INDEX = 103  # array
    TEMP = 104  # temp
    MINUS = 105  # minus
    ERROR = 200


Key = {Tag.IF: 'if',
       Tag.ELSE: 'else',
       Tag.WHILE: 'while',
       Tag.DO: 'do',
       Tag.BREAK: 'break',
       Tag.TRUE: 'true',
       Tag.FALSE: 'false',
       Tag.BASIC: 'basic',
       Tag.LEFTBRACE: '{',
       Tag.RIGHTBRACE: '}',
       Tag.LEFTBRACKETS: '[',
       Tag.RIGHTBRACKETS: ']',
       Tag.LEFTPARENTHESE: '(',
       Tag.RIGHTPARENTHESE: ')',
       Tag.SEMICOLON: ';',
       Tag.ASSIGNMENTOPERATOR: '=',
       Tag.ADDITIONOPERATOR: '+',
       Tag.SUBTRACTIONOPERATOR: '-',
       Tag.MULTIPLICATIONOPERATOR: '*',
       Tag.DIVISIONOPERATOR: '/',
       Tag.LOGICNOT: '!',
       Tag.EQUALOPERATOR: '==',
       Tag.NOTEQUALOPERATOR: '!=',
       Tag.GREATER: '>',
       Tag.LESS: '<',
       Tag.GREATEREQUAL: '>=',
       Tag.LESSEQUAL: '<=',
       Tag.LOGICAND: '&&',
       Tag.LOGICOR: '||',
       Tag.ID: 'id',
       Tag.NUM: 'num',
       Tag.REAL: 'real',
       Tag.END: '#',
       Tag.MINUS: '-'}
