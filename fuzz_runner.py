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
from gen_strategy import GenStrategy
from tqdm.auto import *


class FuzzRunner(object):
    def __init__(self, feed, benchmark='bc', cycle_num=1, file_num=100, timeout=1):
        self._cycle_num = cycle_num
        self._file_num = file_num
        self._timeout = timeout
        self._cur_file = 0
        self._cur_cycle = 0
        self._errors = 0
        self._hangs = 0
        self._exceptions = 0
        self._start_time = 0
        self._gen = GenStrategy(feed, file_num)
        if benchmark == 'bc':
            self._command = 'bc ./input/input{}'
        else:
            self._command = '/usr/local/bin/calc -f ./input/input{}'

    def record_exp(self, exp_file, e):
        os.system('cp input/{0} exp_output/{1}-{2}'.format(exp_file, exp_file, self._cur_cycle))
        with open('exp_output/output', 'a') as f:
            f.write('{0}-{1}'.format(exp_file, self._cur_cycle))
            f.write('\t{}\n'.format(e))

    def run(self):
        bar1 = trange(self._cycle_num)
        self._start_time = datetime.datetime.now()
        for round in bar1:
            self._cur_cycle = round + 1
            bar1.set_description('Total Progress: {0}/{1} Rounds'.format(self._cur_cycle, self._cycle_num))
            self._gen.generate()
            bar2 = trange(self._file_num)
            for i in bar2:
                self._cur_file = i + 1
                bar2.set_description('Round {0} Progress: {1}/{2} Inputs'.format(self._cur_cycle, self._cur_file, self._file_num))
                p = subprocess.Popen(self._command.format(i), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
                t_beginning = time.time() 
                seconds_passed = 0 
                while True: 
                    if p.poll() is not None: 
                        break 
                    seconds_passed = time.time() - t_beginning 
                    if self._timeout and seconds_passed > self._timeout: 
                        p.terminate() 
                        self._hangs += 1
                        break
                message = (str(p.stdout.read())).lower()
                if 'error' in message:
                    self._errors += 1
                if p.returncode and p.returncode != 0:
                    try:
                        subprocess.check_output(self._command.format(i), shell=True)
                    except subprocess.CalledProcessError as e:
                        if 'calc' not in self._command or p.returncode != 1:
                            self._exceptions += 1
                            self.record_exp('input{}'.format(i), e)
                cur_time = (datetime.datetime.now() - self._start_time).seconds
                timing = 'Runtime:  {0} hrs, {1} min, {2} sec'.format(cur_time // 3600, (cur_time - cur_time // 3600) // 60, cur_time % 60) + '\t\t\t\t\t\t\t\t\t\t'
                overall = 'Unique Hangs:  ' + str(self._hangs) + '\t' + 'Unique Crashes:  ' + str(self._exceptions) + '\t' + 'Parse Errors:  ' + str(self._errors)
                progress = timing + overall
                sys.stdout.write('\r' + progress)     

    def get_result(self):
        result = {}
        cur_time = (datetime.datetime.now() - self._start_time).seconds
        result['Elapsed Time'] = '{0} hrs, {1} min, {2} sec'.format(cur_time // 3600, (cur_time - cur_time // 3600) // 60, cur_time % 60)
        result['Total Cycles'] = self._cycle_num
        result['Tested Input'] = self._cycle_num * self._file_num
        result['Parse Errors'] = self._errors
        result['Unique Hangs'] = self._hangs
        result['Unique Crashes'] = self._exceptions
        return result

if __name__ == "__main__":
    runner = Fuzz_runner()
    runner.run()







    