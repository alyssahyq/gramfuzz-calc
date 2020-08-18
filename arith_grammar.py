from gramfuzz.fields import *
from random import randrange

'''bc Precedence
https://www.gnu.org/software/bc/manual/html_mono/bc.html
The expression precedence is as follows: (lowest to highest)

|| operator, left associative
&& operator, left associative
! operator, nonassociative
Relational operators, left associative
Assignment operator, right associative
+ and - operators, left associative
*, / and % operators, left associative
^ operator, right associative
unary - operator, nonassociative
++ and -- operators, nonassociative'''


class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

NDef("int", Int(value=None))
NDef("float",Float(value=None))
NDef("arithmetic_operator",Or('+','-','*','%','/','^'))
NDef("relational_operator",Or('<','<=','>','>=','==','!='))
NDef("boolean_operator",Or('||','&&'))
NDef("assignment_operators", Or('='))
#arith = arithmetic
#repeating patterns for arithmetic operation
arith = Join(NRef("arithmetic_operator"),NRef("int"), sep=" ")
arith_patterns = Join(arith, max=20, sep=" ")
#adding parenthesis for rithmetic operation
arith_paren = Join("(",NRef("int"),arith_patterns,")", sep=" ")
arith_number_paren = Join(NRef("arithmetic_operator"),Or(arith_paren,NRef("int")), sep=" ")
arith_number_paren_patterns = Join(arith_number_paren, max=20, sep=" ")
sqrt = Join("sqrt",arith_paren,sep = '')
#stack to process parenth
Def("bc_input",
    Join(
        Or(arith_paren,NRef("int")),
        arith_number_paren_patterns,
        Opt(Join(NRef("relational_operator"),Or(arith_paren,NRef("int"),sqrt), sep=" ")),
        arith_number_paren_patterns,
    sep=" "),
    cat="bc_input"
)