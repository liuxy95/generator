#! /usr/bin/python

#This program generates CUDA programs according to control knobs
#Author:Zhibin Yu
#Date created: 2015.7.8


import sys
import os
import re
import random


#The workload parameters we will change to form different CUDA programs are:
#Workload Parameters                        Values or range                     Number
#float_alu                                  1..10                                 10
#float_sfu                                  1..8                                  8
#float_mad                                  1..6                                  6
#int_alu                                    1..8                                  8
#int_mad                                    1..6                                  6
#byte_alu                                   1..4                                  4
#loop                                       10...300                              290
#bbsize                                     1..10                                 10
#seed                                       1..10                                 10
#blockDim                                   10..128                               118
#gridDim                                    10..480                               470
#reg_distance                               0..8                                  9
#shared_mem                                 0..8                                  9
#sm_distance                                0..5                                  6
#const_mem                                  0..8                                  8

prog_name = 'CUDA'
f_alu = random.randint(1,10)
f_sfu = random.randint(1,8)
f_mad = random.randint(1,6)
i_alu = random.randint(1,8)
i_mad = random.randint(1,6)
b_alu = random.randint(1,4)
loop = random.randint(10,300)
bbsize = random.randint(1,10)
seed = random.randint(1,10)
b_dim = random.randint(10,128)
g_dim = random.randint(10,480)
r_dist = random.randint(1,8)
sh_mem = random.randint(1,8)
sm_dist = random.randint(1,5)
con_mem = random.randint(1,8)

prog_name = prog_name + '_' + '%d'%f_alu + '_' + '%d'%f_sfu + '_' + '%d'%f_mad + '_' + '%d'%r_dist + '_' + '%d'%i_alu + '_' + '%d'%i_mad + '_' + '%d'%b_alu + '_' + '%d'%loop + '_' + '%d'%bbsize + '_' + '%d'%seed + '_' + '%d'%b_dim + '_' + '%d'%g_dim + '_' + '%d'%sm_dist + '_' + '%d'%sh_mem + '_' + '%d'%con_mem

print prog_name

#command options
options = ' -f ' + prog_name + '.cu' + ' --float_alu=' + '%d'%f_alu + ' --float_sfu=' + '%d'%f_sfu + ' --float_mad=' + '%d'%f_mad + ' --reg_distance=' + '%d'%r_dist + ' --int_alu=' + '%d'%i_alu + ' --int_mad=' + '%d'%i_mad + ' --byte_alu=' + '%d'%b_alu + ' --loop=' + '%d'%loop + ' --bbsize=' + '%d'%bbsize + ' --bbtype=1' + ' --seed=' + '%d'%seed + ' --blockDim=\'' + '%d'%b_dim + ',1,1\'' + ' --gridDim=\'' + '%d'%g_dim + ',1,1\'' + ' --sm_distance=' + '%d'%sm_dist + ' --shared_mem=' + '%d'%sh_mem + ' --const_mem=' + '%d'%con_mem

print 'python py_generator.py' + options

output = os.popen('python py_generator.py' + options)
print output.read()






