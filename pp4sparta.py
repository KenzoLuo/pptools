#!/usr/bin/env python
# pp4sparta.py
# psotprocessing tool for sparta output data
# 1. resave output data as tecplot flie
# 2. compress file size
# 3. surface pressure, shear stress and heat flux (unfinished)
# Kenzo LUO
# 2020.02.10

import numpy as np
import os
import random
import argparse
import matplotlib.pyplot as plt
import sys


# error message
def error(str):
    if str: print("ERROR:", str)
    else: print("Syntax: pp4sparta.py infile headfile outfile keyword args ...")
    sys.exit()


# read_data
def read_data(file_path,frac,cut):
    data_list = []
    with open(file_path, 'r') as f:
        lines_list = f.readlines()
        for lines in lines_list[9:]:
            lines = lines.strip(' \n').split(' ')
            for idx, line in enumerate(lines):
                if (line == 'nan') | (line == '-nan'):
                    lines[idx] = 0
            lines = list(map(float, lines))
            if cut == -1: # do not cut flow box
                if random.random() < frac:
                    data_list.append(lines)
                else:
                    continue
            else:
                if (lines[cut-1] > 1e-6) & (random.random() < frac):
                    data_list.append(lines)
                else:
                    continue
    return data_list


def resave_data(data_list,headfile,outfile):
    with open(headfile, 'r', encoding='utf-8') as hf:
        head_text = hf.readlines()[0]
        # print(head_text)
    with open(outfile, 'w') as f:
        # tecplot data file
        f.write('TITLE ="sparta_data"\n')
        f.write(head_text)
        for idx in range(len(data_list)):
            each_data = map(str, data_list[idx])
            f.write(' '.join(tuple(each_data)) + '\n')
        print("sparta data '%s' resaved. " %(outfile))


if __name__ == '__main__':
    arg = sys.argv
    narg = len(sys.argv)
    if narg < 4: error("")
    infile = arg[1]
    headflie = arg[2]
    outfile = arg[3]

    frac = 1
    cut = -1

    iarg = 4
    while iarg < narg:
        if arg[iarg] == "frac":
            if iarg + 2 > narg: error("frac not be idenfied ")
            frac = float(arg[iarg + 1])
            iarg += 2
        elif arg[iarg] == "cut":
            if iarg + 2 > narg: error("cut_num not be idenfied ")
            cut = int(arg[iarg + 1])
            iarg += 2
        else: error("")

    # data reconstruction
    print("Post-processing start...")
    print("Data read-in start...")
    data_list = read_data(infile,frac,cut)
    print("Data is resaving...")
    resave_data(data_list,headflie,outfile)
    print("Post-processing complete!")

