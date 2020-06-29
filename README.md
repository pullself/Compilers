# Compilers

![](https://img.shields.io/badge/language-python-green.svg)  ![](https://img.shields.io/apm/l/vim-mode.svg)

龙书附录A文法，自底向上LR（1）分析实现

## 环境和依赖

- 环境 python 3.7.4
- 平台 win 10

python依赖：

- prettytable

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
输出词法表

```
python main.py -l {文法文件地址}
```
构造文法分析表

```
python main.py -c {文法文件地址}
```

生成中间代码

```
python main.py -a {代码文件地址}
```

## 中间代码输出格式

```
L1:L3:	i = i + 1
L5:	t1 = i * 8
	t2 = a [ t1 ] 
	if t2 < v goto L3
L4:	j = j - 1
L7:	t3 = j * 8
	t4 = a [ t3 ] 
	if t4 > v goto L4
L6:	if not i >= j goto L8
L9:	goto L2
L8:	t5 = i * 8
	x = a [ t5 ] 
L10:	t6 = i * 8
	t7 = j * 8
	t8 = a [ t7 ] 
	a [ t6 ] = t8
L11:	t9 = j * 8
	a [ t9 ] = x
	goto L1
L2:

```


## 文件结构

```
.
│  action.json //action 表
│  code.txt //代码文件
│  goto.json //goto表
│  grammar.json //文法表
│  grammar.txt //文法文件
│  Intermediate_Language.txt //中间代码输出文件
│  LICENSE
│  main.py //程序入口
│  README.md
│  
└─libs
    │  __init__.py
    │  
    ├─lexers
    │      lexer.py //词法分析器
    │      num.py
    │      real.py
    │      tag.py
    │      token.py
    │      word.py
    │      __init__.py
    │      
    ├─parsers
    │      constructor.py //分析表生成器
    │      data.py
    │      first.py
    │      generator.py
    │      parser.py // 语法分析器
    │      __init__.py
    │      
    ├─rules
    │      access.py
    │      arith.py
    │      constant.py
    │      do.py
    │      expr.py
    │      id.py
    │      logical.py
    │      node.py
    │      op.py
    │      rel.py
    │      seq.py
    │      set.py
    │      setelem.py
    │      stmt.py
    │      temp.py
    │      unary.py
    │      _and.py
    │      _break.py
    │      _else.py
    │      _if.py
    │      _not.py
    │      _or.py
    │      _while.py
    │      __init__.py
    │      
    ├─statistic
    │      code_analyst.py //代码统计工具
    │      visualization.py //输出结果表格工具
    │      __init__.py
    │    
    │          
    └─symbols
           array.py
           env.py
           type.py
           __init__.py

```
