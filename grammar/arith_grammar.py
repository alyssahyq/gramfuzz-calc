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
++ and -- operators, nonassociative

Limits
BC_BASE_MAX
The maximum output base is currently set at 999. The maximum input base is 16.
BC_DIM_MAX
This is currently an arbitrary limit of 65535 as distributed. Your installation may be different.
BC_SCALE_MAX
The number of digits after the decimal point is limited to INT_MAX digits. Also, the number of digits before the decimal point is limited to INT_MAX digits.
BC_STRING_MAX
The limit on the number of characters in a string is INT_MAX characters.
exponent
The value of the exponent in the raise operation (^) is limited to LONG_MAX.
multiply
The multiply routine may yield incorrect results if a number has more than LONG_MAX / 90 total digits. For 32 bit longs, this number is 23,860,929 digits.
variable names
The current limit on the number of unique names is 32767 for each of simple variables, arrays and functions.
'''


class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"
#134217729 is the biggest int that will not trigger "error: exponent too large in raise"
NDef("int", Int(odds = [(0.000000000000001,[0]),(0.99,[-134217729,134217729])]))
NDef("float",Float(odds = [(0.000000000000001,[0]),(0.85,[-100,100])])))
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
