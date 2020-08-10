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


def generate_input():
    fuzzer = gramfuzz.GramFuzzer()
    fuzzer.load_grammar("./bc_grammar.py")
    for i in range(100):
        print('Generating: input{}'.format(i))
        bc_inputs = fuzzer.gen(cat="bc_input", num=1000)
        with open('input{}'.format(i), 'w') as f:
            for bc_input in bc_inputs:
                f.write(bc_input.decode('utf-8') + '\n')
            f.write('quit')
        print('Finished: input{}'.format(i))


if __name__ == "__main__":
    generate_input()
    result = ''
    runtime_error = 0
    exception = 0
    test_num = 0
    for i in range(100):
        try:
            #result = subprocess.check_output(['python', 'except.py'], stderr=subprocess.STDOUT).decode('utf-8')
            result = subprocess.check_output('bc -l input{}'.format(i), shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        except Exception as e:
            result = 'Exception: {}'.format(e);
        finally: 
            #print(result)
            res = result.split('\n')
            for line in res:
                test_num += 1
                if 'error' in line:
                    runtime_error += 1
                if 'Exception' in line:
                    print(line)
                    exception += 1
    print('tested:', test_num, 'error:', runtime_error, 'exception:', exception)
    

