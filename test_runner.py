'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-16 20:06:40
Version: 1.0
'''
import pandas as pd
from ipywidgets import *
import ipywidgets as widgets
from fuzz_runner import *
import time
import sys


benchmarks = ['bc', 'calc']
grammars = ['bc_statement_grammar.py', 'bc_statement_no_loop.py', 'bc_statement_target.py']

def para(Grammar, Benchmark, Rounds, Files, Timeout):
    fuzz_runner = Fuzz_runner('grammar/' + Grammar, Benchmark, Rounds, Files, Timeout)
    start = time.time()
    fuzz_runner.run()
    print('=======================================================================================')
    df = pd.DataFrame(pd.Series(fuzz_runner.get_result()))
    df.columns = ['Values']
    display(df)

def run_widget():
    # Specify the layout of output Box
    form_item_layout = Layout(
        justify_content='space-around',
        margin='2%'
    )
    # Define widgets by interactive and pack into the Box
    form_items = [
        VBox(children=interactive(
            para, 
            {'manual': True}, 
            Grammar=grammars, 
            Benchmark=benchmarks, 
            Rounds=widgets.IntText(1), 
            Files=widgets.IntText(100), 
            Timeout=widgets.IntText(1), 
        ).children, layout=form_item_layout)
    ]
    # Insert items into Box and specify the layout
    form = Box(form_items, layout=Layout(
        display='flex',
        flex_flow='column',
        border='solid 1px',
        align_items='stretch',
        width='750px',
        margin='1.3%'
    ))
    display(form)
   

if __name__ == '__main__':
    run_widget()