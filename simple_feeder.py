'''
@Title:
@Prject:
@Description:
@Author: Sujia Yin
@Date: 2020-07-27 16:31:34
@Version: 1.0
'''
import os
import subprocess
import gramfuzz
import datetime
from pyZZUF.pyZZUF import pyZZUF

file_number = 5 # In every loop, how many input file will be generated and tested.
input_number = 5 # In every file, how many input will be generated according to grammar.

def generate_input(file_path):
    fuzzer = gramfuzz.GramFuzzer()
    fuzzer.load_grammar(file_path)
    for i in range(file_number):
        print('Generating: input{}'.format(i))
        bc_inputs = fuzzer.gen(cat="bc_input", num=input_number)
        with open('input{}'.format(i), 'w') as f:
            for bc_input in bc_inputs:
                f.write(bc_input.decode('utf-8') + '\n')
            f.write('quit')
        #print('Finished: input{}'.format(i))
    print('Finished generated inputs')

def choose_fuzzer(c,file_path):
    if c == 'g':
        generate_input(file_path)
    if c == 'm':
        f = open(file_path)
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
        for i in range(file_number):
            print('Generating: input{}'.format(i))
            zzuf_array =zzuf.mutate()
            bc_input=''
            for j in range(len(zzuf_array)):
                bc_input=bc_input+chr(zzuf_array[j])
            with open('input{}'.format(i), 'w') as f:
                f.write(bc_input)
                f.write('quit')
            # print('Finished: input{}'.format(i))
        print('Finished generated inputs')


def print_time(starttime):
    endtime = datetime.datetime.now()
    second = (endtime-starttime).seconds
    minute = int(second/60)
    hour = int(minute/60)
    if second<60:
        print('Elapsed time: ',second,' seconds.')
    elif minute<60:
        print('Elapsed time: ',minute,' minutes ',second%60,' seconds.')
    else:
        print('Elapsed time: ',hour,' hours ',minute%60,' minutes ',second%60,' seconds.')

if __name__ == "__main__":
    command = ''
    file_path = ''
    c = ''
    while True:
        while (c!='g' and c!='m'):
            c = input("Choose fuzzer: g for grammar-based, m for mutation-based \n")
        benchmark = input("Choose benchmark: b for bc, c for calc \n")
        if benchmark == 'b':
            command = 'bc -l input{}'
            while True:
                grammar = input("Choose grammar: a for arithmetic, s for statement \n")
                if grammar == 'a' and c == 'g':
                    file_path="./grammar/arith_grammar.py"
                    break
                elif grammar == 'a' and c == 'm':
                    file_path="./input/arithmetic_input"
                    break
                elif grammar == 's' and c == 'g':
                    file_path="./grammar/bc_statement_grammar.py"
                    break
                elif grammar == 's' and c == 'm':
                    file_path = "./input/bc_input"
                    break
            break
        elif benchmark == 'c':
            command = 'calc -f input{}'
            while True:
                grammar = input("Choose grammar: a for arithmetic, s for statement \n")
                if grammar == 'a' and c == 'g':
                    file_path="./grammar/arith_grammar.py"
                    break
                elif grammar == 'a' and c == 'm':
                    file_path="./input/arithmetic_input"
                    break
                elif grammar == 's' and c == 'g':
                    file_path="./grammar/calc_statement_grammar.py"
                    break
                elif grammar == 's' and c == 'm':
                    file_path = "./input/calc_input"
                    break
            break
    count = 0
    tested_sum = 0
    error_sum = 0
    exception_sum = 0
    starttime = datetime.datetime.now()
    while True:
        if (exception_sum > 0):
            break
        choose_fuzzer(c,file_path)
        result = ''
        runtime_error = 0
        exception = 0
        test_num = 0
        for i in range(file_number):
            try:
                # result = subprocess.check_output(['python', 'except.py'], stderr=subprocess.STDOUT).decode('utf-8')
                result = subprocess.check_output('command'.format(i), shell=True, stderr=subprocess.STDOUT).decode(
                    'utf-8')
                print("input",i,"tested.")
            except Exception as e:
                result = 'Exception: {}'.format(e);
            finally:
                # print(result)
                res = result.split('\n')
                for line in res:
                    test_num += 1
                    if 'error' in line:
                        runtime_error += 1
                    if 'Exception' in line:
                        print(line)
                        exception += 1
        tested_sum = tested_sum + test_num
        error_sum = error_sum + runtime_error
        exception_sum = exception_sum + exception
        count = count+1
        print('Loop ', count)
        print('tested_sum', tested_sum)
        print('error_sum', error_sum)
        print('exception_sum', exception_sum)
        #print('tested:', tested_sum, 'error:', error_sum, 'exception:', exception_sum)
        print_time(starttime)


