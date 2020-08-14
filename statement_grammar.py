from gramfuzz.fields import *
from random import randrange

'''bc Precedence
https://www.gnu.org/software/bc/manual/html_mono/bc.html
The expression precedence is as follows: (lowest to highest)'''


class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

NDef('int',Int(odds = [(0.05,[0]),(0.85,[-100,100])])) # INT_MAX
array_ind = Or(0,1,2,3,4,5,6,7,8,9)
function_name = Or('fun0','fun1','fun2','fun3','fun4','fun5','fun6','fun7','fun8','fun9')
variable_name = Or('a','b','c','d','e')
variable_odd = Or(Join(variable_name,'[]',sep=''),
                  variable_name,variable_name,variable_name,variable_name,variable_name,variable_name,
                  Join(variable_name,'[',array_ind,']',sep=''))
var_post = Join(variable_odd,Or('++','--'),sep='')
var_pre = Join(Or('++','--'),variable_odd,sep='')

assign_operation = Or('=','+=','-=','*=','/=','^=','%=')
arith_operation = Or('+','-','*','/','%','^')
arith_expr = Join(Or(variable_odd,NRef('int')),
                  Join(Join(arith_operation,Or(variable_odd,NRef('int')),sep='')
                      ,max=5,sep='')
                  ,sep='')
assign = Or(Join(variable_odd,assign_operation,Or(variable_odd,NRef('int')),sep=' '))

expr_operation = Or('>','<','>=','<=','==','!=')
condition = Join(arith_expr,expr_operation,arith_expr,sep=' ')

auto = Join('auto',variable_odd,Opt(Join(',',variable_odd,sep=' ')),sep=' ')

if_else = Join('if (',condition,'){','\n',
               Join(Or(auto,assign,assign,assign,assign,assign),max=5,sep='\n'),'}','\n',
               Opt(Join('else{','\n',
                        Join(Or(auto,assign,assign,assign,assign,assign),max=5,sep='\n'),'}',sep='')),
               sep=''
)

for_loop = Join('for(',Or(assign,variable_odd),';',condition,';',assign,'){','\n',
                Join(Or(auto,assign),max=5,sep='\n'),'\n',
                Opt(Join('if (',condition,'){','\n',
                         Join(Or(auto,assign,assign,assign,assign,assign,assign,'break','continue'),max=5,sep='\n'),'}','\n',
                         Opt(Join('else{','\n',
                                  Join(Or(auto,assign,'break','continue'),max=5,sep='\n'),'}',sep='')),sep='')),
                '}'
                ,sep='')

while_loop = Join('while(',condition,'){','\n',
                Join(Or(auto,assign,assign,assign,assign,assign,assign),'\n',max=5,sep='\n'),'\n',
                Opt(Join('if (',condition,'){','\n',
                         Join(Or(auto,assign,assign,assign,assign,assign,'break','continue'),max=5,sep='\n'),'}','\n',
                         Opt(Join('else{','\n',
                                  Join(Or(auto,assign,assign,assign,assign,assign,assign,'break','continue'),max=5,sep='\n'),'}',sep='')),sep='')),
                '}'
                ,sep='')

variable_list = Join(variable_odd,
                     Opt(Join(
                         Join(',',variable_odd,sep='')
                         ,max=5,sep=''))
                     ,sep='')
def_fun = Join('define ',function_name,'(',variable_list,'){','\n',
               Join(Or(while_loop,assign,assign,assign,assign,assign,for_loop,auto,if_else),max=5,sep='\n'),
               Opt(Join('return ',Or(variable_odd,NRef('int')),'\n',sep='')),'}'
               ,sep='')

Def("bc_input",
    Join(Or(def_fun,while_loop,assign,for_loop,auto,if_else),max=10,sep="\n"),
    cat="bc_input"
)
