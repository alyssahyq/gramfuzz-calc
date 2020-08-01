import gramfuzz

fuzzer = gramfuzz.GramFuzzer()
fuzzer.load_grammar("./bc_grammar.py")
bc_inputs = fuzzer.gen(cat="bc_input", num=10)
#should dump them into a file
for bc_input in bc_inputs:
    print(bc_input.decode("utf-8"))