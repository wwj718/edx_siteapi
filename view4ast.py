#!/usr/bin/env python
# encoding: utf-8

import inspect
import ast
import codegen  #需要安装
from ast_fun import hello
print "*"*10

expr_str = inspect.getsource(hello)
expr_ast =ast.parse(expr_str)
#ast.dump(expr_ast)
#old = expr_ast.body[0]
function_def = expr_ast.body[0]
new_return =  ast.parse("return 'wwj'").body[0]
#fun_return  = function_def.body[-1]
function_def.body[-1] = new_return
#new_return =  ast.parse("return 'wwj'").body[0]
#fun_return = new_return
source = codegen.to_source(expr_ast)
print source
#全局变量c没有导入
#ns = {} #上下文
#exec code in ns
exec(source, globals())
print hello()

