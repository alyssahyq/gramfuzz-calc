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
assign_array = Join(array,'={',Join(NRef('int'),sep=',',max=statement_max),sep='')
array_i = Join(variable_name,'[',array_ind,']',sep='')
var_post = Join(Or(variable_name,variable_name,variable_name,array_i),Or('++','--'),sep='')
var_pre = Join(Or('++','--'),Or(variable_name,variable_name,variable_name,array_i),sep='')
variable_list = Or(array,array,variable_name,variable_name,variable_name,array_i,var_post,var_pre)
para_list = Join(variable_list,max=statement_max ,sep=',')
call_function = Join(function_name,'(',para_list,')',sep='')
variable_odd =  Or(array,array,variable_name,variable_name,variable_name,array_i,call_function,call_function,call_function,
                   var_post,var_pre)
print=Join('print(',variable_odd,')',sep='')
assign_operation = Or('=','+=','-=','*=','/=','^=','%=')
arith_operation = Or('+','-','*','/','%','^')
arith_expr = Join(Or(variable_odd,NRef('int')),
                  Opt(Join(Join(arith_operation,Or(variable_odd,NRef('int')),sep='')
                      ,max=statement_max,sep=''))
                  ,sep='')
assign = Join(variable_odd,assign_operation,arith_expr,sep=' ')

expr_operation = Or('>','<','>=','<=','==','!=')
condition = Join(arith_expr,expr_operation,arith_expr,sep=' ')

auto = Join('auto',Join(variable_odd,max=statement_max,sep=','),sep=' ')

statement = Join(Or(auto,assign,assign,assign,call_function,call_function,assign_array,print),max=statement_max,sep='\n')


if_else = Join('if (',condition,'){','\n',
               statement,'}','\n',
               Opt(Join('else{','\n',
                        statement,'}',sep='')),
               sep=''
)

for_loop = Join('for(',Or(assign,variable_odd),';',condition,';',assign,'){','\n',
               statement,'\n',
                Opt(Join('if (',condition,'){','\n',
                         Join(Or(auto,assign,assign,assign,call_function,call_function,'break','continue')
                              ,max=statement_max,sep='\n'),'}','\n',
                         Opt(Join('else{','\n',
                                  Join(Or(auto,assign,assign,assign,call_function,call_function,'break','continue')
                                       ,max=statement_max,sep='\n'),'}',sep='')),sep='')),
                '}'
                ,sep='')

while_loop = Join('while(',condition,'){','\n',
                statement,'\n',
                Opt(Join('if (',condition,'){','\n',
                         Join(Or(auto,assign,assign,assign,call_function,call_function,'break','continue')
                              ,max=statement_max,sep='\n'),'}','\n',
                         Opt(Join('else{','\n',
                                  Join(Or(auto,assign,assign,assign,call_function,call_function,'break','continue')
                                       ,max=statement_max,sep='\n'),'}',sep='')),sep='')),
                '}'
                ,sep='')

#max in def_fun: in
def_fun = Join('define ',function_name,'(',para_list,'){','\n',
               Join(Or(while_loop,statement,statement,statement,for_loop,if_else),max=statement_max,sep='\n'),'\n',
               Opt(Join('return ',Or(variable_odd,NRef('int')),'\n',sep='')),'}'
               ,sep='')

Def("bc_input",
    Join(Or(def_fun,while_loop,assign,call_function,for_loop,auto,if_else),max=statement_max,sep="\n"),
    cat="bc_input"
)
