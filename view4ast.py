#!/usr/bin/env python
# encoding: utf-8

import inspect
import ast
import codegen  #需要安装

def hello():
    a=2
    b=3
    print a+b
    return a+b
print hello()

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
exec(source, globals())
print hello()

