from gramfuzz.fields import *
from random import randrange

'''bc Precedence
https://www.gnu.org/software/bc/manual/html_mono/bc.html
The expression precedence is as follows: (lowest to highest)'''

# No loop, No ^

class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

statement_max = 5 # Maximum of the times the elements occur in this part randomly


array_ind = Or(0,1,2,3,4,5,6,7,8,9)
function_name = Or('fun0','fun1','fun2')
variable_name = Or('a','b','c','d')
array = Join(variable_name,'[]',sep='')
variable_list = Or(array,variable_name)
para_list = Join(variable_list,max=statement_max ,sep=',')
call_function = Join(function_name,'(',para_list,')',sep='')
variable_odd =  Or(array,variable_name)

assign_operation = Or('=','+=','-=','*=',)
assign = Or(Join(variable_odd,assign_operation,variable_odd,sep=' '))

statement = Join(Or(assign,assign,assign,call_function,call_function),max=statement_max,sep='\n')

#max in def_fun: in
def_fun = Join('define ',function_name,'(',para_list,'){','\n',
               statement,'\n',
               Opt(Join('return ',variable_odd,'\n',sep='')),'}'
               ,sep='')

Def("bc_input",
    Join(Or(def_fun,statement,statement,statement),max=statement_max,sep="\n"),
    cat="bc_input"
)
