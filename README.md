# Compilers

![](https://img.shields.io/badge/language-python-green.svg)  ![](https://img.shields.io/apm/l/vim-mode.svg)

龙书附录A文法，自底向上LR（1）分析实现

## 环境

- 环境 python 3.7.4
- 平台 win 10

## 功能

- 自动根据文法生成LR（1）分析表
- 使用分析表生成中间代码

## 文法格式要求

上下文无关文法，左部非终结符+符号`->`+右部，右部每个独立终结符/非终结符用空格隔开

eg：
```
type->type [ num ]|basic
stmts->stmts stmt|ε
stmt->loc = bool ;|if ( bool ) stmt|if ( bool ) stmt else stmt|while ( bool ) stmt|do stmt while ( bool ) ;|break ;|block
```

## 使用方法
构造文法分析表

```
python main.py -c {文法文件地址}
```

生成中间代码

```
python main.py -a {代码文件地址}
```

