'''
Title: 
Prject: 
Description: 
Author: Sujia Yin
Date: 2020-08-14 18:49:24
Version: 1.0
'''
import os
import time
import datetime
import subprocess
import pandas as pd
import sys
from generator import *
from tqdm.auto import *


class Fuzz_runner(object):
    def __init__(self, grammar, benchmark='bc', cycle_num=1, file_num=100, timeout=1):
        self.cycle_num = cycle_num
        self.file_num = file_num
        self.timeout = timeout
        self.cur_file = 0
        self.cur_cycle = 0
        self.errors = 0
        self.hangs = 0
        self.exceptions = 0
        self.start_time = 0
        self.gen = Generator(grammar, file_num)
        if benchmark == 'bc':
            self.command = 'bc ./input/input{}'
        else:
            self.command = 'calc -f ./input/input{}'

    def record_exp(self, exp_file, e):
        os.system('cp input/{0} exp_output/{1}-{2}'.format(exp_file, exp_file, self.cur_cycle))
        with open('exp_output/output', 'a') as f:
            f.write(exp_file)
            f.write('\t{}\n'.format(e))

    def run(self):
        bar1 = trange(self.cycle_num)
        self.start_time = datetime.datetime.now()
        for round in bar1:
            self.cur_cycle = round + 1
            bar1.set_description('Total Progress: {0}/{1} Rounds'.format(self.cur_cycle, self.cycle_num))
            self.gen.generate()
            bar2 = trange(self.gen.file_num)
            for i in bar2:
                self.cur_file = i + 1
                bar2.set_description('Round Progress: {0}/{1} Inputs'.format(self.cur_file, self.file_num))
                p = subprocess.Popen(self.command.format(i), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
                t_beginning = time.time() 
                seconds_passed = 0 
                while True: 
                    if p.poll() is not None: 
                        break 
                    seconds_passed = time.time() - t_beginning 
                    if self.timeout and seconds_passed > self.timeout: 
                        p.terminate() 
                        self.hangs += 1
                        break
                rtcode = p.returncode
                if rtcode:
                    if 'error' in p.stdout.read().decode('utf-8'):
                        self.errors += 1
                    if rtcode != 0:
                        self.exceptions += 1
                        try:
                            subprocess.check_output('bc t', shell=True)
                        except subprocess.CalledProcessError as e:
                            self.record_exp('input{}'.format(i), e)
                cur_time = (datetime.datetime.now() - self.start_time).seconds
                timing = 'Runtime:  {0} hrs, {1} min, {2} sec'.format(cur_time // 3600, (cur_time - cur_time // 3600) // 60, cur_time % 60) + '\t\t\t\t\t\t\t\t\t\t'
                overall = 'Unique Hangs:  ' + str(self.hangs) + '\t' + 'Unique Crashes:  ' + str(self.exceptions) + '\t' + 'Interpreting Errors:  ' + str(self.errors)
                progress = timing + overall
                sys.stdout.write('\r' + progress)     

    def get_result(self):
        result = {}
        cur_time = (datetime.datetime.now() - self.start_time).seconds
        result['Elapsed Time'] = '{0} hrs, {1} min, {2} sec'.format(cur_time // 3600, (cur_time - cur_time // 3600) // 60, cur_time % 60)
        result['Total Cycles'] = self.cycle_num
        result['Tested Input'] = self.cycle_num * self.file_num
        result['Interpret Errors'] = self.errors
        result['Unique Hangs'] = self.hangs
        result['Unique Crashes'] = self.exceptions
        return result

if __name__ == "__main__":
    runner = Fuzz_runner()
    runner.run()







    