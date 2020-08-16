# gramfuzz-calc
We plan to specify grammars of inputs for three selected benchmarks, which share similar API and grammars of inputs. Then we will use these grammars as the seeds to generate well-formated inputs via gramfuzz, a Python-based grammer fuzzer, to penetrate deep into benchmarks’ parsers. We expect that some potential errors of benchmarks would be detected in this project. In addition, we plan to design a runner program, which can feed the inputs into the benchmarks automatically, as enhancements to gramfuzz.

## Grammar files:
* General use
    - arith_grammar.py: Grammar of arithmetic calculation, suits bc, calc and qalc
* bc
    - bc_statement_grammar.py: Grammar of bc statements, including defining/calling functions, assignment statements, if-else, while loop, for loop.
    - bc_statement_no_loop.py: No loop and exponential calculation, avoiding infinite loops or long calculation time
    - bc_statement_target.py: Grammar of found bugs.
