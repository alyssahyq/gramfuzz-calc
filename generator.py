'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-14 21:43:19
Version: 1.0
'''
import gramfuzz
from pyZZUF.pyZZUF import pyZZUF


class Generator(object):
    def __init__(self, feed, file_num):
        self._feed = feed
        self._file_num = file_num
    
    def genetate(self):
        pass

class GramGenerator(Generator):
    def generate(self):
        fuzzer = gramfuzz.GramFuzzer()
        fuzzer.load_grammar(self._feed)
        for i in range(self._file_num):
            bc_inputs = fuzzer.gen(cat="bc_input", num=1)
            with open('input/input{}'.format(i), 'w') as f:
                for bc_input in bc_inputs:
                    f.write(bc_input.decode('utf-8') + '\n')
                f.write('quit')

class MutateGenerator(Generator):
    def generate(self):
        f = open(self._feed)
        seed_input = f.read()
        seed_byte = seed_input.encode('utf-8')
        zzuf = pyZZUF(seed_byte)
        f.close()
        zzuf.set_protected('quit', True)
        zzuf.set_protected('if', True)
        zzuf.set_protected('else', True)
        zzuf.set_protected('define', True)
        zzuf.set_protected('auto', True)
        zzuf.set_protected('local', True)
        zzuf.set_protected('{', True)
        zzuf.set_protected('}', True)
        for i in range(self._file_num):
            zzuf_array =zzuf.mutate()
            bc_input=''
            for j in range(len(zzuf_array)):
                bc_input=bc_input+chr(zzuf_array[j])
            with open('input/input{}'.format(i), 'w') as f:
                f.write(bc_input)
                f.write('quit')
