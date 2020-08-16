from gramfuzz.fields import *
from random import randrange

'''bc Precedence
https://www.gnu.org/software/bc/manual/html_mono/bc.html
The expression precedence is as follows: (lowest to highest)'''


class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

statement_max = 5 # Maximum of the times the elements occur in this part randomly

NDef('int',Int(odds = [(0.05,[0]),(0.85,[-100,100])])) # INT_MAX
array_ind = Or(0,1,2,3,4,5,6,7,8,9)
function_name = Or('fun0','fun1','fun2','fun3','fun4')
variable_name = Or('a','b','c','d')
array = Join(variable_name,'[]',sep='')
array_i = Join(variable_name,'[',array_ind,']',sep='')
var_post = Join(Or(variable_name,variable_name,variable_name,array_i),Or('++','--'),sep='')
var_pre = Join(Or('++','--'),Or(variable_name,variable_name,variable_name,array_i),sep='')
variable_list = Or(array,array,variable_name,variable_name,variable_name,array_i,var_post,var_pre)
call_function = Join(function_name,'(',variable_list')',sep='')
variable_odd =  Or(array,array,variable_name,variable_name,variable_name,array_i,call_function,call_function,call_function,
                   var_post,var_pre)


assign_operation = Or('=','+=','-=','*=','/=','%=')
arith_operation = Or('+','-','*','/','%')
arith_expr = Join(Or(variable_odd,NRef('int')),
                  Join(Join(arith_operation,Or(variable_odd,NRef('int')),sep='')
                      ,max=statement_max,sep='')
                  ,sep='')
assign = Or(Join(variable_odd,assign_operation,Or(variable_odd,NRef('int')),sep=' '))

expr_operation = Or('>','<','>=','<=','==','!=')
condition = Join(arith_expr,expr_operation,arith_expr,sep=' ')

auto = Join('auto',variable_odd,Opt(Join(',',variable_odd,sep=' ')),sep=' ')

if_else = Join('if (',condition,'){','\n',
               Join(Or(auto,assign,assign,assign,assign,assign),max=statement_max,sep='\n'),'}','\n',
               Opt(Join('else{','\n',
                        Join(Or(auto,assign,assign,assign,assign,assign),max=statement_max,sep='\n'),'}',sep='')),
               sep=''
)

variable_list = Join(variable_odd,
                     Opt(Join(
                         Join(',',variable_odd,sep='')
                         ,max=statement_max,sep=''))
                     ,sep='')

#max in def_fun: in
def_fun = Join('define ',function_name,'(',variable_list,'){','\n',
               Join(Or(assign,assign,assign,assign,assign,auto,if_else),max=statement_max,sep='\n'),
               Opt(Join('return ',Or(variable_odd,NRef('int')),'\n',sep='')),'}'
               ,sep='')

Def("bc_input",
    Join(Or(def_fun,def_fun,def_fun,assign,assign,assign,auto,if_else),max=statement_max,sep="\n"),
    cat="bc_input"
)
