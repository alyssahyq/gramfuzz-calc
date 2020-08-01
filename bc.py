import os
import subprocess
import gramfuzz

def generate_input():
    fuzzer = gramfuzz.GramFuzzer()
    fuzzer.load_grammar("./bc_grammar.py")
    bc_inputs = fuzzer.gen(cat="bc_input", num=10)
    with open('input', 'w') as f:
        for bc_input in bc_inputs:
            f.write(bc_input.decode('utf-8') + '\n')
        f.write('quit')

if __name__ == "__main__":
    generate_input()
    result = subprocess.check_output(['bc', 'input'], stderr=subprocess.STDOUT).decode('utf-8')
    print(result)
