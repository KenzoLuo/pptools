# ds2vpp.py
# psotprocessing tool for ds2v output data
# 1. profile of Couette flow
# 2. stagnation streamline
# 3. surface pressure, shear stress and heat flux (unfinished)
# 4. profile of the blunt shear flow
# Kenzo LUO
# 2020.02.04

import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
plt.switch_backend('agg')


# error message

def error(str):
    if str: print("ERROR:", str)
    else: print("Syntax: pp4ds2v.py style blunt/couette/surf keyword args ...")
    sys.exit()


def read_data_ds2ff(file_path):
    ds2ff_list = []
    with open(file_path, 'r') as f:
        lines_list = f.readlines()
        for lines in lines_list[2:]:
            lines = lines.strip('\n').split()
            lines = ' '.join((lines)).split(' ')
            if 'ZONE' in lines:
                break
            for idx, line in enumerate(lines):
                if line == 'NaN':
                    lines[idx] = 0
            lines = list(map(float, lines))
            assert len(lines) == 19, 'unnormal cols'
            if lines[2] < 0.000001:
                continue
            ds2ff_list.append(lines)
    return ds2ff_list


def read_data_ds2su(file_path):
    ds2su_list = []
    with open(file_path, 'r') as f:
        lines_list = f.readlines()
        for lines in lines_list[2:]:
            lines = lines.strip('\n').split()
            lines = ' '.join((lines)).split(' ')
            if 'ZONE' in lines:
                break
            lines = list(map(float, lines))
            ds2su_list.append(lines)
    return ds2su_list


# processing for couette flow
def pack_data(data_sort_arr):
    profile_list = []
    pre_idx, pre_y = 0, data_sort_arr[0][1]
    for idx in range(1, len(data_sort_arr), 1):
        cur_y = data_sort_arr[idx, 1]
        if cur_y != pre_y:
            each_data = data_sort_arr[pre_idx:idx, :]
            profile_list.append(list(np.mean(each_data, axis=0)))
            pre_idx = idx
            pre_y = cur_y
    each_data = data_sort_arr[pre_idx:, :]
    profile_list.append(list(np.mean(each_data, axis=0)))
    return profile_list


def visualize_couette(outfile):
    with open(outfile, 'r') as f:
        data = f.readlines()
    y_list, ttra_list, trot_list, tvib_list, u_list = list(), list(), list(), list(), list()
    for line in data[1:]:
        y_value, ttra_value, trot_value, tvib_value, u_value = tuple(
            map(float, line.split(' ')[:5]))
        y_list.append(y_value)
        ttra_list.append(ttra_value)
        trot_list.append(trot_value)
        tvib_list.append(tvib_value)
        u_list.append(u_value)

    plt.subplots()
    plt.plot(ttra_list, y_list, label='Ttra')
    plt.plot(trot_list, y_list, label='Trot')
    plt.plot(tvib_list, y_list, label='Tvib')
    plt.grid(True)
    plt.legend(loc='lower right', fontsize='large')
    plt.xlabel('T(K)')
    plt.ylabel('y(m)')
    plt.savefig('temp_profile.png')
    # plt.show()
    plt.cla()
    plt.plot(u_list, y_list, label='u')
    plt.grid(True)
    plt.legend(loc='lower right', fontsize='large')
    plt.xlabel('u(m/s)')
    plt.ylabel('y(m)')
    plt.savefig('u_profile.png')
    print('couette visualization images saved. ')


def resave_data_couette(profile_list):
    profile_arr = np.array(profile_list)
    if uptemp != 1:
        # ttra = (profile_arr[:, 7] - 300) / (args.uptemp - 300)
        # trot = (profile_arr[:, 8] - 300) / (args.uptemp - 300)
        ttra = profile_arr[:, 7] / uptemp
        trot = profile_arr[:, 8] / uptemp
    else:
        ttra = profile_arr[:, 7]
        trot = profile_arr[:, 8]
    if uptvib != 1:
        tvib = (profile_arr[:, 9] - 300) / (uptvib - 300)
    else:
        tvib = profile_arr[:, 9]
    u = profile_arr[:, 4] / upu
    y = profile_arr[:, 1]
    p = profile_arr[:, 18]
    n = profile_arr[:, 2]

    with open(outfile, 'w') as f:
        # OriginLab data file
        f.write('y ttra trot tvib u p n\n')
        for idx in range(len(profile_list)):
            each_data = map(
                str, [y[idx], ttra[idx], trot[idx], tvib[idx], u[idx], p[idx], n[idx]])
            f.write(' '.join(tuple(each_data)) + '\n')
    print('OriginLab data resaved. ')


def cal_heat_flux_wall(ds2su_list):
    # Heat flux to the wall
    ds2su_list_arr = np.array(ds2su_list)
    heat_flux = np.mean(ds2su_list_arr[:, 9])
    # heat_flux_var = np.std(ds2su_list_arr[:, 9], ddof=1)
    print('Heat FLux to the wall = %.2f ' % (heat_flux))


def pp4couette(ds2ff_list, ds2su_list):
    ds2ff_sort_list = sorted(ds2ff_list, key=lambda i: i[1])  # sort by 'y'
    ds2ff_sort_arr = np.array(ds2ff_sort_list)
    profile_list = pack_data(ds2ff_sort_arr)  # average in x direction
    resave_data_couette(profile_list)
    visualize_couette(outfile)
    cal_heat_flux_wall(ds2su_list)


# processing for blunt flow
def extract_sl_data(ds2ff_list):
    ds2ff_sort_list = sorted(ds2ff_list, key=lambda i: i[1])  # sort by 'y'
    ds2ff_sort_arr = np.array(ds2ff_sort_list)
    stag_line_list = []
    max_y = ds2ff_sort_arr[len(ds2ff_sort_arr) - 1][1]
    err_y = 0.01*max_y
    idx, cur_y = 0, ds2ff_sort_arr[0, 1]
    while cur_y < err_y:
        each_data = ds2ff_sort_arr[idx, :]
        stag_line_list.append(each_data)
        idx, cur_y = idx + 1, ds2ff_sort_arr[idx, 1]
    print('%d points of the stag_stream line are extracted!' % len(stag_line_list))
    return stag_line_list


def extract_shear_profile(ds2ff_list):
    # profile through (0.55,0.17)
    ds2ff_sort_list = sorted(ds2ff_list, key=lambda i: i[0])  # sort by 'x'
    ds2ff_sort_arr = np.array(ds2ff_sort_list)
    shear_prof_list = []
    x1 = ds2ff_sort_arr[len(ds2ff_sort_arr) - 1][0]
    y1 = ds2ff_sort_arr[len(ds2ff_sort_arr) - 1][1]
    for idx in range(len(ds2ff_sort_arr) - 1, 1, -1):
        if abs((x1 - 0.3)*1 + (y1 - 0.1)*0.16) < 0.001:
            each_data = ds2ff_sort_arr[idx, :]
            shear_prof_list.append(each_data)
        x1 = ds2ff_sort_arr[idx, 0]
        y1 = ds2ff_sort_arr[idx, 1]   
    print('%d points of the shear profile are extracted!' % len(shear_prof_list))
    shear_prof_list = sorted(shear_prof_list, key=lambda i: i[1])
    shear_prof_arr = np.array(shear_prof_list)
    ttra = shear_prof_arr[:, 7]
    trot = shear_prof_arr[:, 8]
    tvib = shear_prof_arr[:, 9]
    y = shear_prof_arr[:, 1]
    plt.figure()
    plt.scatter(ttra, y, label='Ttra', s=15, alpha=0.6)
    plt.scatter(trot, y, label='Trot', s=15, alpha=0.6)
    plt.scatter(tvib, y, label='Tvib', s=15, alpha=0.6)
    plt.grid(True)
    plt.legend(loc='best', fontsize='large')
    plt.xlabel('T(K)')
    plt.ylabel('y(m)')
    plt.savefig('shear_profile.png')
    print('shear_profile visualization images saved. ')
    # print('unfinished')
    return shear_prof_list


def visualize_stag_line(stag_line_list):
    stag_line_list = sorted(stag_line_list, key=lambda i: i[0])
    stag_line_arr = np.array(stag_line_list)
    ttra = stag_line_arr[:, 7]
    trot = stag_line_arr[:, 8]
    tvib = stag_line_arr[:, 9]
    x = stag_line_arr[:, 0]
    # u = stag_line_arr[:, 4]
    # p = stag_line_arr[:, 18]
    # n = stag_line_arr[:, 2]

    # fig, ax = plt.subplots()
    plt.figure()
    plt.plot(x, ttra, label='Ttra')
    plt.plot(x, trot, label='Trot')
    plt.plot(x, tvib, label='Tvib')
    plt.grid(True)
    plt.legend(loc='best', fontsize='large')
    plt.xlabel('T(K)')
    plt.ylabel('y(m)')
    plt.savefig('temp_sl.png')
    print('stag_line visualization images saved. ')


def resave_data_blunt(ds2ff_list):
    with open(outfile, 'w') as f:
        # tecplot data file
        f.write('TITLE ="stagnation_flow"\n')
        f.write(
            'VARIABLES= x y n den u v w Ttra Trot Tvib T ma mc mct mfp sof fsp ang p \n')
        for idx in range(len(ds2ff_list)):
            each_data = map(str, ds2ff_list[idx])
            f.write(' '.join(tuple(each_data)) + '\n')
        print('Tecplot data resaved. ')


def cal_heat_flux_stag(ds2su_list):
    # Stagnation point heat flux
    ds2su_sort_list = sorted(ds2su_list, key=lambda i: i[2])
    ds2su_arr = np.array(ds2su_sort_list)
    len_of_surf = len(ds2su_sort_list)
    s = ds2su_arr[int(0.05*len_of_surf):int(0.35*len_of_surf), 1]
    q = ds2su_arr[int(0.05*len_of_surf):int(0.35*len_of_surf), 9]
    z1 = np.polyfit(s, q, 1)
    heat_flux = z1[1]
    print('Heat FLux to Stag Point = %.2f ' % (heat_flux))


def pp4blunt(ds2ff_list, ds2su_list):
    stag_line_list = extract_sl_data(ds2ff_list)
    resave_data_blunt(ds2ff_list)
    visualize_stag_line(stag_line_list)
    cal_heat_flux_stag(ds2su_list)
    if prof == 'yes':
        extract_shear_profile(ds2ff_list)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='detect table lines')
    # parser.add_argument('style', type=str, help='the path of input file.')
    # parser.add_argument('--resave', type=str,
    #                     help='the resaved file.', default='resaved.dat')
    # parser.add_argument('--prof', type=str,
    #                     help='extract flow profile in the shear flow or not, "yes" or "no". ', default='no')
    # parser.add_argument('--upu', type=int,
    #                     help='the velocity of upper boundary', default=1)
    # parser.add_argument('--uptemp', type=int,
    #                     help='the temperature of upper boundary', default=1)
    # parser.add_argument('--uptvib', type=int,
    #                     help='the vibrational temp of upper boundary', default=1)
    # args = parser.parse_args()

    arg = sys.argv
    narg = len(sys.argv)
    # print (narg)
    if narg < 3: error("1")
    style = arg[2]
    
    outfile = "resaved.dat"
    prof = "no"

    iarg = 3
    while iarg < narg:
        if arg[iarg] == "outfile":
            if iarg + 2 > narg: error("outfile path not defined")
            outfile = arg[iarg + 1]
            iarg += 2
        elif arg[iarg] == "prof":
            print ("bug")
            if iarg + 2 > narg: error("prof arg err")
            prof = arg[iarg + 1]
            iarg += 2
        elif arg[iarg] == "norm":
            if iarg + 4 > narg: error("norm should be followed by 'upu uptemp uptvib' ")
            upu = float(arg[iarg + 1])
            uptemp = float(arg[iarg + 2])
            uptvib = float(arg[iarg + 3])
            iarg += 4
        else: error("2")

    # data reconstruction
    ds2ff_list = read_data_ds2ff('DS2FF.DAT')
    ds2su_list = read_data_ds2su('DS2SU.DAT')

    # switch postprocessing style
    if style == 'couette':
        pp4couette(ds2ff_list, ds2su_list)
    elif style == 'blunt':
        pp4blunt(ds2ff_list, ds2su_list)
    else:
        error('pp style should be "couette" or "blunt", postprocessing abort! ')
