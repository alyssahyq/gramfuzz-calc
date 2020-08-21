'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-14 21:43:19
Version: 1.0
'''
import abc
import gramfuzz
import random
from pyZZUF.pyZZUF import pyZZUF


class Generator(metaclass = abc.ABCMeta):
    def __init__(self, feed, file_num):
        self._feed = feed
        self._file_num = file_num
    
    @abc.abstractclassmethod
    def generate(self):
        pass


class GramGenerator(Generator):
    def generate(self):
        print('\nGenerating seeds...')
        fuzzer = gramfuzz.GramFuzzer()
        fuzzer.load_grammar(self._feed)
        for i in range(self._file_num):
            bc_inputs = fuzzer.gen(cat="bc_input", num=1)
            with open('input/input{}'.format(i), 'w') as f:
                for bc_input in bc_inputs:
                    f.write(bc_input.decode('utf-8') + '\n')
                f.write('quit')
        print('{} files generated. Start fuzzing...'.format(self._file_num))


class MutateGenerator(Generator):
    def generate(self):
        print('\nGenerating seeds...')
        f = open(self._feed)
        seed_input = f.read()
        f.close()
        for i in range(self._file_num):
            seed_byte = seed_input.encode('utf-8')
            zzuf = pyZZUF(seed_byte, random.randint(0, 100), random.uniform(0.004, 0.1), None)
            zzuf.set_protected('quit', True)
            zzuf.set_protected('if', True)
            zzuf.set_protected('else', True)
            zzuf.set_protected('define', True)
            zzuf.set_protected('auto', True)
            zzuf.set_protected('local', True)
            zzuf.set_protected('{', True)
            zzuf.set_protected('}', True)
            zzuf_array = zzuf.mutate()
            bc_input = ''
            for j in range(len(zzuf_array)):
                bc_input += chr(zzuf_array[j])
            with open('input/input{}'.format(i), 'w') as f:
                f.write(bc_input)
        print('{} files generated. Start fuzzing...'.format(self._file_num))
        
        
