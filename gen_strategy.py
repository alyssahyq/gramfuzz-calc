'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-18 17:58:46
Version: 1.0
'''
from generator import *

class GenStrategy(object):
    def __init__(self, feed, file_num):
        self._file_num = file_num
        if 'grammar' in feed:
            self._generator = GramGenerator(feed, file_num)
        else:
            self._generator = MutateGenerator(feed, file_num)

    def generate(self):
        print('\nGenerating seeds...')
        self._generator.generate()
        print('{} files generated. Start fuzzing...'.format(self._file_num))
