'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-14 21:43:19
Version: 1.0
'''
import gramfuzz

class Generator(object):
    def __init__(self, file_num=100):
        self.file_num = file_num

    def generate(self):
        fuzzer = gramfuzz.GramFuzzer()
        fuzzer.load_grammar("./statement_grammar.py")
        for i in range(self.file_num):
            bc_inputs = fuzzer.gen(cat="bc_input", num=1)
            with open('./input/input{}'.format(i), 'w') as f:
                for bc_input in bc_inputs:
                    f.write(bc_input.decode('utf-8') + '\n')
                f.write('quit')
