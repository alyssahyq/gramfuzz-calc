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
    while True:
        benchmark = input("Choose benchmark: b for bc, c for calc, q for qalc \n")
        if benchmark == 'b':
            command = 'bc -l input{}'
            while True:
                grammar = input("Choose grammar: a for arithmetic, s for statement, n for no loop, t for target \n")
                if grammar == 'a':
                    file_path="./grammar/arith_grammar.py"
                    break
                elif grammar == 's':
                    file_path="./grammar/bc_statement_grammar.py"
                    break
            break
        elif benchmark == 'c':
            command = 'calc -f input{}'
            while True:
                grammar = input("Choose grammar: a for arithmetic, s for statement \n")
                if grammar == 'a':
                    file_path="./grammar/arith_grammar.py"
                    break
                elif grammar == 's':
                    file_path="./grammar/calc_statement_grammar.py"
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
        generate_input(file_path)
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


