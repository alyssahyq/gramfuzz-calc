# gramfuzz-calc
We build a grammar-based fuzzer using [gramfuzz](https://github.com/d0c-s4vage/gramfuzz) and a mutation-based fuzzer using [pyZZUF](https://github.com/nezlooy/pyZZUF). And we designed a runner program to select the program-under-test, [bc](https://www.gnu.org/software/bc/manual/html_mono/bc.html) or [calc](https://www.systutorials.com/docs/linux/man/1-calc/), and its grammar, arithmetic calulation or program statement, feed the inputs automatically, save suspicious inputs and display the testing status in an interface.

## Run our runner program
```
jupyter notebook interface.ipynb
```
The results will be saved in ./exp_out
