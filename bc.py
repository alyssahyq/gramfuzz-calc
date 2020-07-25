import gramfuzz

fuzzer = gramfuzz.GramFuzzer()
fuzzer.load_grammar("./bc_grammar.py")
names = fuzzer.gen(cat="name", num=10)
for name in names:
    print(str(name))