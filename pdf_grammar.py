from gramfuzz.fields import *
from random import randrange

class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

NDef("header", Or('%PDF-1.8','%PDF-1.7','%PDF-1.6','%PDF-1.5','%PDF-1.4','%PDF-1.3','%PDF-1.2','%PDF-1.1','%PDF-1.0'))

NDef("int", Int(value=None))
NDef("float",Float(value=None))
NDef("boolean",Or(True,False))
NDef("ascii",String(charset=''.join([chr(i) for i in range(128)]),max=200))
stream = Join('(',NRef("ascii"),')',sep='')
object_stream =  Join('stream',stream,'endstream',sep='\n')
object_streams = Join(object_stream,sep='\n',max = 10)
NDef("escape",Or('\n','\r','\t','\b','\f','\(','\)','\\','\ddd'))
NDef("hexadecimal",String(charset='ABCEDF0123456789'))
ascii_hash = Join('#',NRef("hexadecimal"),NRef("hexadecimal"),sep='')
name = Join()
indirect = Join(NRef('int'),' 0',' obj','\n',
                '\t','\Type',Or('/Pages','/Catalog'),
                Or(object_streams),'\n',
                'endobj','\n',sep='')
trailer = Join("trailer",'\n',
               '<<','\Size',NRef('int'),'\n',
               Or(Join('\Prev',NRef('int'),'\n',sep=' ')),
               '\Root',NRef('int'),'0','\n',
               '\n','>>',sep=' ')
cross_reference = Join("startxref",NRef('int'),"%%EOF",sep='\n')
#stack to process parenth
Def("bc_input",
    Join(
        NRef("header"),
        object_streams,
        trailer,
        cross_reference,
    sep="\n"),
    cat="random_pdf"
)

