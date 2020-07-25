import gramfuzz

fuzzer = gramfuzz.GramFuzzer()
fuzzer.load_grammar("./bc_grammar.py")
exprs = fuzzer.gen(cat="expr", num=10)
for expr in exprs:
    print(expr.decode("utf-8"))
