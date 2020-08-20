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
from fuzz_runner import FuzzRunner
from generator import GramGenerator, MutateGenerator


benchmarks = ['bc', 'calc']
fuzzer = ['', 'gramFuzz', 'zzuf']
grammars = ['arith_grammar.py', 'bc_statement_grammar.py', 'calc_statement_grammar.py']
seeds = ['arithmetic_input', 'bc_input', 'calc_input']

def fuzz_type(Fuzzer):
    run_widget(Fuzzer)

def para(Feed, Benchmark, Rounds, Files, Timeout):
    if 'grammar' in Feed:
        fuzz_runner = FuzzRunner(GramGenerator, 'gram_seed/' + Feed, Benchmark, Rounds, Files, Timeout)
    else:
        fuzz_runner = FuzzRunner(MutateGenerator, 'gram_seed/' + Feed, Benchmark, Rounds, Files, Timeout)
    fuzz_runner.run()
    print('==================================================================================')
    df = pd.DataFrame(pd.Series(fuzz_runner.get_result()))
    df.columns = ['Values']
    display(df)

def select_fuzzer():
    # Specify the layout of output Box
    form_item_layout = Layout(
        justify_content='space-around',
        margin='2%'
    )
    # Define widgets by interactive and pack into the Box
    form_items = [
        VBox(children = interactive(
            fuzz_type, 
            {'manual': False}, 
            Fuzzer = fuzzer, 
        ).children, layout = form_item_layout)
    ]
    # Insert items into Box and specify the layout
    form = Box(form_items, layout=Layout(
        display = 'flex',
        flex_flow = 'column',
        border = 'solid 1px',
        align_items = 'stretch',
        width = '750px',
        margin = '1.3%'
    ))
    display(form)
    

def run_widget(Fuzzer):
    # Specify the layout of output Box
    form_item_layout = Layout(
        justify_content = 'space-around',
        margin = '2%'
    )
    # Define widgets by interactive and pack into the Box
    form_items = []
    if Fuzzer == 'gramFuzz':
        form_items.append(
            VBox(children = interactive(
                para, 
                {'manual': True}, 
                Feed = grammars, 
                Benchmark = benchmarks, 
                Rounds = widgets.IntText(1), 
                Files = widgets.IntText(100), 
                Timeout = widgets.IntText(1), 
            ).children, layout = form_item_layout)
        )
    elif Fuzzer == 'zzuf':
        form_items.append(
            VBox(children = interactive(
                para, 
                {'manual': True}, 
                Feed = seeds, 
                Benchmark = benchmarks, 
                Rounds = widgets.IntText(1), 
                Files = widgets.IntText(100), 
                Timeout = widgets.IntText(1), 
            ).children, layout = form_item_layout)
        )
    else:
        print('Please select a fuzzer type!')
    # Insert items into Box and specify the layout
    form = Box(form_items, layout = Layout(
        display = 'flex',
        flex_flow = 'column',
        align_items = 'stretch',
        width = '720px',
        margin = '1.3%'
    ))
    display(form)
   