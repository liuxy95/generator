#! /usr/bin/python

## This file is created by Zhibin Yu on April 22, 2015 and it is used to generate configurations for GPGPU_sim.
import sys
import os
import re
import random

# users must input a parameter when using this script
if len(sys.argv) < 2:
	print 'please input a parameter'
	sys.exit()

# the configure file name is the first parameter of this script
fname = sys.argv[1]
eva = fname.find('.config')
suf = fname[eva:]
tr = cmp(suf,'.config')
if tr:
	print 'Please input a configuration file as the first parameter!'
	sys.exit()

f = open(fname,'r')
flist = f.readlines()
f.close()

#The architectural parameters we will change to form different GPGPU architecture configurations are:
#Archiectural parameters					values				      Number
#gpgpu_shader_cta                       1,2,4,8,16                      5
#core_frequency                         0.5,0.6,0.7,0.8,0.9,1.0GHz      6
#interconnect_frequency                 0.5,0.6,0.7,0.8,0.9,1.0GHz      6
#L2 cache frequency                     0.5,0.6,0.7,0.8,0.9,1.0GHz      6
#DRAM frequency                         0.5,0.6,0.7,0.8,0.9,1.0GHz      6
#shader registers                       4,8,16,32,64K                   5         Note:K=1024
#max_warp_core                          32,40,48,56,64                  5
#L1 DCache                              2,4,8,16,32KB                   5
#shmem(shared memory)                   2,4,8,16,32KB                   5
#L2 DCache                              16,32,48,64,80KB                5
#L1 ICache                              1,2,4,8,16KB                    5
#L1 tex Cache                           3,6,12,18,24KB                  5
#L1 con Cache(const cache)              2,4,6,8,10KB                    5
#DRAM queue                             8,16,24,32,40,48                6

shader_cta=['1','2','4','8','16']
core_freq=['500.0','600.0','700.0','800.0','900.0','1000.0']
intcon_freq=['500.0','600.0','700.0','800.0','900.0','1000.0']
l2_freq=['500.0','600.0','700.0','800.0','900.0','1000.0']
dram_freq=['724.0','824.0','924.0','1024.0','1124.0','1224.0']
sm_reg=['16384','24576','32768','40960','49152','57344','65536']

#Note that in GPGPU-sim, the max warps per core can not be larger than 48 which is WARP_PER_CTA_MAX=48
max_wc=['1024','1152','1280','1408','1536']    # max warps per core. 1024 for 32,1152 for 36,1280 for 40, 1408 for 44, and 1536 for 48
l1d=['4','8','16','32','64']                   # L1 Data Cache size. 4 sets for 2KB, 8 for 4KB, 16 for 8KB,32 for 16KB, and 64 for 32KB 
l1i=['2','4','8','16','32']                    # L1 Instruction Cache size. 2 sets for 1KB, 4 for 2KB,8 for 4KB,16 for 8KB,and 32 for 16KB
shmem=['16384','24576','32768','40960','49152','57344','65536']                  # shared memory size
l2d=['16','32','48','64','80','96']            # L2 Data Cache size
l1tex=['1','2','4','6','8']                    # L1 texture cache size. 1 set for 3KB, 2 for 6KB, 4 for 12KB, 6 for 18KB and 8 for 24KB
l1con=['16','32','48','64','80']               # L1 const cache size. 16 sets for 2KB,32 for 4KB, 48 for 6KB, 64 for 8KB and 80 for 10KB
dramq=['8','16','24','32','40','48']           # dram scheduler queue size
dramrq=['64','72','80','88','96','104']        # dram scheduler return queue size

k = 0
for item in flist:
	# randomly choose a value for -gpgpu_shader_cta
	if ~item.find('-gpgpu_shader_cta'):
		r = random.randint(0,4)
		npos = item.index(' ')
		item = item[0:npos]
		item = item + ' ' + shader_cta[r]
		flist[k] = item + '\n'

	# randomly choose frequences for -gpgpu_clock_domains
    # currently I use the same value for core, interconnect, L2 cache frequence and that for dram is 200.0MHz larger
	if ~item.find('-gpgpu_clock_domains') and item.find('#'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,5)
		item = item + ' ' + core_freq[r] + ':' + intcon_freq[r] + ':' + l2_freq[r] + ':' + dram_freq[r]
		flist[k] = item + '\n'

	# randomly choose the number of regsiters for a shader core.  -gpgpu_shader_registers
	if ~item.find('-gpgpu_shader_registers'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,6)
		item = item + ' ' + sm_reg[r] + '\n'
		flist[k] = item
	
	# randomly choose the max number of warps per-core. set the number before ':' in '-gpgpu_shader_core_pipeline 1536:32'
	if ~item.find('-gpgpu_shader_core_pipeline'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,4)
		item = item + ' ' + max_wc[r] + ':32' + '\n'
		flist[k] = item
	
	# randomly set the L1 data cache size. There are several parameters such as nset, assoc, and line size. I only change the nset
	if ~item.find('-gpgpu_cache:dl1') and item.find('#'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,4)
		item = item + ' ' + l1d[r] + ':128:4,L:L:m:N,A:32:8,8' + '\n'
		flist[k] = item
	
	# randomly set the L1 instruction cache size. Like the L1 data cache, I only change the nset
   	if ~item.find('-gpgpu_cache:il1'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,4)
		item = item + ' ' + l1i[r] + ':128:4,L:R:f:N,A:2:32,4' + '\n'
		flist[k] = item

	# randomly set the size of shared memory.
	if ~item.find('-gpgpu_shmem_size') and item.find('#'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,6)
		item = item + ' ' + shmem[r] + '\n'
		flist[k] = item

	# randomly set the L2 data cache size. Like the L1 data cache, I only change the nset
	if ~item.find('-gpgpu_cache:dl2') and item.find('-gpgpu_cache:dl2_texture_only'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,5)
		item = item + ' ' + l2d[r] + ':128:8,L:B:m:W,A:32:4,4:0,32' + '\n'
		flist[k] = item

	# randomly set the L1 texture cache size. Like the L1 data cache. I only change the nset
	if ~item.find('-gpgpu_tex_cache:l1'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,4)
		item = item + ' ' + l1tex[r] + ':128:24,L:R:m:N,F:128:4,128:2' + '\n'
		flist[k] = item

	# randomly set the L1 const cache size. Like the L1 data cache. I only change the nset
	if ~item.find('-gpgpu_const_cache:l1'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,4)
		item = item + ' ' + l1con[r] + ':64:2,L:R:f:N,A:2:32,4' + '\n'
		flist[k] = item

	# randomly set the dram scheduler queue size.
	if ~item.find('-gpgpu_frfcfs_dram_sched_queue_size'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,5)
		item = item + ' ' + dramq[r] + '\n'
		flist[k] = item
	
	# randomly set the dram scheduler return queue size.
	if ~item.find('-gpgpu_dram_return_queue_size'):
		npos = item.index(' ')
		item = item[0:npos]
		r = random.randint(0,5)
		item = item + ' ' + dramrq[r] + '\n'
		flist[k] = item
	k = k + 1
ff = open(fname,'w')
ff.writelines(flist)
ff.close()
