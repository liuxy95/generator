#!/usr/bin/python
import os,sys
import getopt
import random

insn_list={
'add.float.alu':['add',2,'f64'],
'sub.float.alu':['sub',2,'f64'],
'mul.float.alu':['mul',2,'f64'],
'div.float.alu':['div.rn',2,'f64'],
'min.float.alu':['min',2,'f64'],
'max.float.alu':['max',2,'f64'],
'neg.float.alu':['neg',1,'f64'],
'sqrt.float.sfu':['sqrt.rn',1,'f64'],
'abs.float.alu':['abs',1,'f64'],
#'sin.float.sfu':['sin.approx',1,'f64'],
#'cos.float.sfu':['cos.approx',1,'f64'],
#'ex2.float.sfu':['ex2.approx',1,'f64'],
#'lg2.float.sfu':['lg2.approx',1,'f64'],
'rsqrt.float.sfu':['rsqrt.approx',1,'f64'],
'rcp.float.sfu':['rcp.rn',1,'f64'],
'fma.float.mad':['fma.rn',3,'f64'],
'mad.float.mad':['mad.rn',3,'f64'],
'not.byte.alu':['not',1,'b32'],
'or.byte.alu':['or',2,'b32'],
'and.byte.alu':['and',2,'b32'],
#'popc.byte.alu':['popc',1,'b32'],
'xor.byte.alu':['xor',2,'b32'],
'abs.int.alu':['abs',1,'s32'],
'neg.int.alu':['neg',1,'s32'],
'shr.int.alu':['shr',2,'s32'],
'shl.byte.alu':['shl',2,'b32'],
'add.int.alu':['add',2,'s32'],
'sub.int.alu':['sub',2,'s32'],
'mul.int.alu':['mul.lo',2,'s32'],
'div.int.alu':['div',2,'s32'],
'rem.int.alu':['rem',2,'s32'],
'min.int.alu':['min',2,'s32'],
'max.int.alu':['max',2,'s32'],
'sad.int.alu':['sad',3,'s32'],
'mad.int.mad':['mad.lo',3,'s32']
}

f_alu_list=['add','sub','mul','div','min','max','neg','abs']
f_mad_list=['mad','fma']
f_sfu_list=['sqrt','rsqrt','rcp']
d_alu_list=['add','sub','mul','div','min','max','neg','abs','rem','sad','shr']
d_mad_list=['mad']
b_alu_list=['not','or','and','xor','shl']

#d_alu_list=[]
#d_sfu_list=[]

f_list=[e.split('.')[0] for e in insn_list.keys() if e.find('float')!=-1]
d_list=[e.split('.')[0] for e in insn_list.keys() if e.find('int')!=-1]
b_list=[e.split('.')[0] for e in insn_list.keys() if e.find('byte')!=-1]

#print f_list
#print d_list
#print b_list
t_r={
'int':['%rd','%d_0','%d_1','%ropd3'],
'float':['%rf','%f_0','%f_1','%ropf3'],
'byte':['%rb','%ropb0','%ropb1']
}
#instruction class
class Intructions:
	def __init__(self):
		self.name='add';
		self.prefix=self.name;
		self.op_type='float';
		self.num_op=1
		self.dst='null'
		self.insn=''
		self.insn_num='0'
		self.insn_type='alu'

	def setInsn(self,name,op_type,insn_type,insn_num,dst='null'):
		self.name=name;
		self.op_type=op_type;
		self.dst=dst;
		self.insn_num=insn_num;
		self.insn_type=insn_type;
		self.prefix=insn_list[name+'.'+op_type+'.'+insn_type][0]+'.'+insn_list[name+'.'+op_type+'.'+insn_type][2]
		self.num_op=insn_list[name+'.'+op_type+'.'+insn_type][1]
		
	def getInsn(self):
		insn=self.prefix+'\t'
		t_r_l=t_r[self.op_type]	
		tmp_dst=t_r_l[0]+self.insn_num
		if self.dst!='null':
			tmp_dst=self.dst;
		#num of operands
		if self.num_op==1:
			insn +=tmp_dst+', '+t_r_l[random.randint(1,2)]+';'
		elif self.num_op==2:
			insn +=tmp_dst+', '+t_r_l[1]+', '+t_r_l[2]+';'
		else:
			insn +=tmp_dst+', '+t_r_l[1]+', '+t_r_l[2]+', '+t_r_l[3]+';'
		return insn;
	
	# set register dependency distance
	def getInsnOP(self,op1,op2,op3,d=3):
		insn=self.prefix+'\t'
		t_r_l=t_r[self.op_type]
		tmp_dst=t_r_l[0]+self.insn_num
		if self.dst!='null':
			tmp_dst=self.dst;
		reg='';
		rtype='';
		if self.op_type=='float':
			reg='%rf'
			rtype='%f_'
		elif self.op_type=='int':
			reg='%rd'
			rtype='%d_'
		else:
			reg='%rb'
			rtype='%ropb'
		#num of operands
		if self.num_op==1:
			if self.name=='rsqrt' or self.name=='rcp':
				insn += tmp_dst+', '+rtype+str(random.randint(0,1))+';'
			else:
				insn += tmp_dst+', '+reg+str(op1)+';'
		elif self.num_op==2:
			if self.name=='div' or self.name=='rem':
				insn += tmp_dst+', '+reg+str(op1)+', '+rtype+str(random.randint(0,1))+';'
			else:
				if d>=2:
					insn += tmp_dst+', '+reg+str(op1)+', '+reg+str(op2)+';'
				else:
					insn += tmp_dst+', '+reg+str(op1)+', '+rtype+str(random.randint(0,1))+';'
		else:
			if d>=3:
				insn += tmp_dst+', '+reg+str(op1)+', '+reg+str(op2)+', '+reg+str(op3)+';'
			elif d==2:
				insn += tmp_dst+', '+reg+str(op1)+', '+reg+str(op2)+', '+rtype+str(random.randint(0,1))+';'
			else:
				insn += tmp_dst+', '+reg+str(op1)+', '+rtype+str(0)+', '+rtype+str(1)+';'	

		return insn;

#code generator
class Generator:
	def __init__(self):
		# source file_stream name
		self.fname='';
		# the structure type of basic block
		self.bbtype=1;
		# average basic block size
		self.bbsize=10;
		# grid size
		self.gridDim=[1,1,1];
		# block size
		self.blockDim=[1,1,1];
		
		# instruction type
		self.n_f=0;#num of float insn. range 1-4
		self.n_d=0;#num of int insn. range 1-4
		self.n_b=0;#num of byte insn. range 1-2;
		#instruction mix
		self.add=0;
		self.sub=0;
		self.mul=0;
		self.div=0;
		self.sqrt=0;
		self.lg=0;
		self.exp=0;
		self.sin=0;
		self.cos=0;
		self.abs=0;
		self.mad=0;
		self.mov=0;
		self.fma=0;
		#instruction mix
		self.f_alu=0;
		self.f_mad=0;
		self.f_sfu=0;
		self.d_alu=0;
		self.d_mad=0;
		self.b_alu=0;
		#register dependency distance
		self.reg_distance=0;
		# global memory instructions
		self.ld_gl=0; #global LD instruction ratio
		self.st_gl=0; #global st instrction ratio
		
		# shared memory instructions
		self.ld_shd=0; #shared LD instruction ratio
		self.st_shd=0; #shared ST instruction ratio
		self.shared_mem=0; #shared memory enable
		self.sm_distance=0;  #distance between a st and a load
		# const memory
		self.const_mem=0; #const memory enable
		#working set size
		self.loop=0;
		#seed
		self.seed=0;
		
		#mid results
		self.n_regs=10;
		self.n_inst=10;
		self.fcounter=0;
		self.dcounter=0;
		self.bcounter=0;
		self.pcounter=0;

	#usage of this script
	def usage(self):
		print "python generate.py [options]:"
		print "\t--fname: file_stream name"
		print "\t--bbtype: basic block type"
		print "\t--gridDim: grid size, number of blocks in a grid"
		print "\t--blockDim: block size, number of threads in a block"
		print "\t--bbsize: average basic block size"
		print "\t--loop: number of loops"
		print "\t--ld_gl: number of global load instructions"
		print "\t--st_gl: number of global store instructions"
		print "\t--ld_shd: number of shared load instructions"
		print "\t--st_shd: number of shared store instructions"
		print "\t--seed: number of random seeds"
		print "\t--add,--sub,--sin,--mad,--mul,--div,--abs,--lg,--sqrt:instruction mix"

	def getParameter(self):
		arg_names=['help','fname=','bbtype=','gridDim=','blockDim=','bbsize=','add=','sub=','mul=','div=','sqrt=','lg=','sin=','mad=','mov=','abs=','ld_gl=','st_gl=','loop=','seed=','num_float=','num_int=','num_byte=','float_alu=','float_sfu=','float_mad=','int_alu=','int_mad=','byte_alu=','reg_distance=','const_mem=','shared_mem=','sm_distance='];
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'hf:', arg_names)
		except getopt.GetoptError, err:
			print str(err)
			sys.exit(2);
		for o,e in opts:
			if(o=='-h' or o=='--help'):
				self.usage();
				sys.exit(2);
			if(o=='-f' or o=='--fname'):
				self.fname=e;
			if(o=='--bbtype'):
				self.bbtype=int(e)
			if(o=='--bbsize'):
				self.bbsize=int(e)
				self.n_regs=int(e)
			if(o=='--seed'):
				self.seed=int(e)
			if(o=='--loop'):
				self.loop=int(e)
			if(o=='--ld_gl'):
				self.ld_gl=int(e)
			if(o=='--st_gl'):
				self.st_gl=int(e)
			if(o=='--ld_shd'):
				self.ld_shd=int(e)
			if(o=='--st_shd'):
				self.st_shd=int(e)
			if(o=='--gridDim'):
				l1=e.split(',')
				self.gridDim=[int(l) for l in l1]
			if(o=='--blockDim'):
				l2=e.split(',')
				self.blockDim=[int(l) for l in l2]
			if(o=='--add'):
				self.add=int(e)
			if(o=='--sub'):
				self.sub=int(e)
			if(o=='--mul'):
				self.mul=int(e)
			if(o=='--div'):
				self.div=int(e)
			if(o=='--sqrt'):
				self.sqrt=int(e)
			if(o=='--lg'):
				self.lg=int(e)
			if(o=='--sin'):
				self.sin=int(e)
			if(o=='--mad'):
				self.mad=int(e)
			if(o=='--mov'):
				self.mov=int(e)
			if(o=='--abs'):
				self.abs=int(e)
			if(o=='--sm_distance'):
				self.sm_distance=int(e)
			if(o=='--reg_distance'):
				self.reg_distance=int(e)
			if(o=='--exp'):
				self.exp=int(e)
			if(o=='--float_alu'):#alu float
				self.f_alu=float(e)
			if(o=='--float_sfu'):#sfu float
				self.f_sfu=float(e)
			if(o=='--float_mad'):#mad float
				self.f_mad=float(e)
			if(o=='--int_alu'):#alu int
				self.d_alu=float(e)
			if(o=='--int_mad'):#mad int
				self.d_mad=float(e)
			if(o=='--byte_alu'):#logic byte
				self.b_alu=float(e)
			if(o=='--shared_mem'):#logic byte
				self.shared_mem=int(e)
				self.ld_shd=int(e)
				self.st_shd=int(e)
			if(o=='--const_mem'):#logic byte
				self.const_mem=int(e)

		self.n_inst = self.bbtype * self.bbsize;
		tmp_sum = self.f_alu + self.f_sfu + self.f_mad + self.d_alu + self.d_mad + self.b_alu;
		self.f_alu = int(self.f_alu * self.n_regs / tmp_sum);
		self.f_mad = int(self.f_mad * self.n_regs / tmp_sum);
		self.f_sfu = int(self.f_sfu * self.n_regs / tmp_sum);
		self.d_alu = int(self.d_alu * self.n_regs / tmp_sum);
		self.d_mad = int(self.d_mad * self.n_regs / tmp_sum);
		self.b_alu = int(self.b_alu * self.n_regs / tmp_sum);

	def genUnUsedKernel(self,file_stream):
		file_stream.write(
		"//this is an unused kernel\n"
		"__global__ void kk(float * d)\n"
		"{\n"
		"\td[0]=kconst[0];"
		"}\n\n"
		)
	#write the head of the source file_stream
	def genHead(self,file_stream):
		file_stream.write(
			"//This is a generated CUDA code\n"+
			"#include<stdio.h>\n"
			"#include<stdlib.h>\n"
			"#include<time.h>\n\n"
		)

		if self.const_mem>0:
			file_stream.write(self.declareConstMem()+"\n\n")
			self.genUnUsedKernel(file_stream)
		
		file_stream.write(
			"\n__global__ void kernel(float*,float*,float*,int*,int*,int *,int);\n"
			"float uniform(float start,float end)\n"
			"{\n"
			"\treturn start+(end-start)*rand()/RAND_MAX;\n"
			"}\n\n"
			"int main(int argc, char* argv[])\n"
			"{\n"
			"\tint gridx = "+str(self.gridDim[0])+";\n"
			"\tint gridy = "+str(self.gridDim[1])+";\n"
			"\tint gridz = "+str(self.gridDim[2])+";\n"
			"\tint bx = "+str(self.blockDim[0])+";\n"
			"\tint by = "+str(self.blockDim[1])+";\n"
			"\tint bz = "+str(self.blockDim[2])+";\n"
			"\n"
			"\tdim3 gridDim(gridx,gridy,gridz);\n"
			"\tdim3 blockDim(bx,by,bz);\n"
			"\n"
			"\t//srand( (unsigned)time( NULL ) );\n"
			"\tsrand("+str(self.seed)+");\n"
    	)

	#declare the shared memory to stress the shared memory
	# %s_mem
	def declareSharedMem(self,file_stream):
		bsize=self.blockDim[0]*self.blockDim[1]*self.blockDim[2];
		file_stream.write(
			'\tasm volatile(".shared .align 4 .b8 __shared_mem__['+str(4*bsize)+'];\\n\\\n'
			'\t.reg .u64    %s_base;\\n\\\n'
			'\t.reg .u64    %s_offset;\\n\\\n'
			'\t.reg .u64    %s_mem;\\n\\\n'
			'\tmov.u64  %s_base,__shared_mem__;\\n\\\n'
			'\tmul.wide.u32   %s_offset,%rbtid,4;\\n\\\n'
			'\tadd.u64  %s_mem,%s_base,%s_offset;");\n\n'
		)
	
	#generate shared memory store
	def genSharedMemST(self,file_stream,src):
		file_stream.write(
			'\tst.shared.f64  [%s_mem+0],'+src+';\\n\\\n'
		)
	#generate shared memory load
	def genSharedMemLD(self,file_stream,dst):
		file_stream.write(
			'\tld.shared.f64	'+dst+', [%s_mem+0];\\n\\\n'
		)
		
	#declare the constant memory to stress the constant
	# %c_mem
	def declareConstMem(self):
		bsize=self.blockDim[0]*self.blockDim[1]*self.blockDim[2];
		ss='__constant__ float kconst['+str(bsize)+'] = {\n'
		for i in range(bsize):
			if i==bsize-1:
				ss += str(random.uniform(10,10000))+'\n';
				continue;
			if (i+1)%8==0:
				ss += str(random.uniform(10,10000))+',\n';
			else:
				ss += str(random.uniform(10,10000))+',';

		ss += '};\n'
		return ss;
	# generate constant memory space
	def genConstMem(self,file_stream):
		bsize=self.blockDim[0]*self.blockDim[1]*self.blockDim[2];
		file_stream.write(
			'\tasm volatile(".reg .u64    %c_base;\\n\\\n'
			'\t.reg .u64    %c_offset;\\n\\\n'
			'\t.reg .u64    %c_mem;\\n\\\n'
			'\tmov.u64  %c_base,kconst;\\n\\\n'
			'\tmul.wide.u32   %c_offset,%rbtid,4;\\n\\\n'
			'\tadd.u64  %c_mem,%c_base,%c_offset;");\n\n'
		)
	#generate constant memory load
	def genConstMemLD(self,file_stream,dst):
		file_stream.write(
			'\tld.const.f64	'+dst+', [%c_mem+0];\\n\\\n'
		)
		
	#delcear the float pointers
	def declareFloatP(self,file_stream):
		file_stream.write(
			"\t//declare variables\n"
			"\tint N=64,size=0,loop=0;\n\n"
			"\t//initialize the variables\n"
			"\tN=gridx*gridy*gridz*bx*by*bz;\n"
			"\tloop="+str(self.loop)+";\n\n"
			"\tN=gridx*gridy*gridz*bx*by*bz*"+str(self.loop+1)+";\n"
			"\tsize=(N)*sizeof(float);\n"
			"\t//declare the float pointer variables\n"
			"\tfloat * f0,*fd0,*f1,*fd1,*f2,*fd2;\n"
		)
	
	def initFloatP(self,file_stream):
		tmp=['0','1','2']
		for i in tmp:
			file_stream.write(
				"\t//parameter f"+i+"\n"
				"\tf"+i+"=(float*)malloc(size);\n"
				"\tmemset(f"+i+",0,size);\n"
            	"\tcudaMalloc((void**)&fd"+i+",size);\n"
				"\tfor(int i=0;i<N;i++)\n"
				"\tf"+i+"[i]=uniform(1,10000);\n"
				"\tcudaMemcpy(fd"+i+",f"+i+",size,cudaMemcpyHostToDevice);\n\n"
			)

	def declareIntP(self,file_stream):
		file_stream.write(
			"\t//declare the int pointer variables\n"
			"\tint * d0,*dd0,*d1,*dd1,*d2,*dd2;\n"
			"\tsize=(N)*sizeof(int);\n\n"
		)
	
	def initIntP(self,file_stream):
		tmp=['0','1','2']
		for i in tmp:
			file_stream.write(
				"\t//parameter d"+i+"\n"
				"\td"+i+"=(int*)malloc(size);\n"
				"\tmemset(d"+i+",0,size);\n"
				"\tcudaMalloc((void**)&dd"+i+",size);\n"
				"\tfor(int i=0;i<N;i++)\n"
				"\td"+i+"[i]=uniform(1,10000);\n"
				"\tcudaMemcpy(dd"+i+",d"+i+",size,cudaMemcpyHostToDevice);\n\n"
			)
		#file_stream.flush()

	def callKernel(self,file_stream):
		file_stream.write(
			"\tkernel<<<gridx*gridy,bx*by*bz>>>(fd0,fd1,fd2,dd0,dd1,dd2,loop);\n\n"
		)
	
	def printResult(self,file_stream):
		tmp=['d','f']
		for e in tmp:
			file_stream.write(
				'\tcudaMemcpy('+e+'2,'+e+'d2, size, cudaMemcpyDeviceToHost);\n'
				'\t/*for(int i=0;i<N;i++)\n'
				'\t\tprintf("%'+e+'\t",'+e+'2[i]);\n'
				'\tprintf("\\n");*/\n'
			)
		file_stream.write('}\n')
	
	def genKernel(self,file_stream):
		
		file_stream.write('\n__global__ void kernel(float* f0,float* f1,float* f2,int *d0,int *d1,int *d2,int loop)\n'
				'{\n'
		)
		file_stream.write(
			'\t//declear the regs\n'
			'\tasm volatile(".reg .u32	%rt<4>;\\n\\\n' #regs used for threadId
				'\t.reg .u32 %rnt<4>;\\n\\\n'				#regs used for blocksize
				'\t.reg .u32 %rc<4>;\\n\\\n'				#regs used for blockId
				'\t.reg .u32 %rnc<4>;\\n\\\n'				#regs used for gridsize
				'\t.reg .u32 %rg<14>;\\n\\\n'				#regs used for compute global threadID
				'\t.reg .u32 %rgtid;\\n\\\n'				#global threadID
				'\t.reg .u32 %rbtid;");\n'					#block threadID
			'\t//compute global threadID\n'
			'\tasm volatile("mov.u32	%rt1,%tid.x;\\n\\\n'	#threadId.x
				'\tmov.u32	%rt2,%tid.y;\\n\\\n'					#threadId.y
				'\tmov.u32	%rt3,%tid.z;\\n\\\n'					#threadId.z
				'\tmov.u32	%rnt1,%ntid.x;\\n\\\n'					#blocksize.x
				'\tmov.u32	%rnt2,%ntid.y;\\n\\\n'					#blocksize.y
				'\tmov.u32	%rnt3,%ntid.z;\\n\\\n'					#blocksize.z
				'\tmov.u32	%rc1,%ctaid.x;\\n\\\n'					#blockId.x
				'\tmov.u32	%rc2,%ctaid.y;\\n\\\n'					#blockId.y
				'\tmov.u32	%rc3,%ctaid.z;\\n\\\n'					#blockId.z
				'\tmov.u32	%rnc1,%nctaid.x;\\n\\\n'				#gridsize.x
				'\tmov.u32	%rnc2,%nctaid.y;\\n\\\n'				#gridsize.y
				'\tmov.u32	%rnc3,%nctaid.z;");'						#gridsize.z
			'\t//compute threadID in a block\n'
			'\tasm volatile("mul.lo.u32	%rg1,%rnt1,%rnt2;\\n\\\n'	#rg1=ntid.x*ntid.y
				'\tmul.lo.u32	%rg2,%rg1,%rt3;\\n\\\n'					#rg2=tid.z*ntid.x*ntid.y
				'\tmul.lo.u32	%rg3,%rt2,%rnt1;\\n\\\n'				#rg3=tid.y*ntid.x
				'\tadd.u32	%rg4,%rt1,%rg3;\\n\\\n'						#rg4=tid.x+tid.y*ntid.x
				'\tadd.u32	%rg5,%rg4,%rg2;\\n\\\n'						#rg5=tid.x+tid.y*ntid.x+tid.z*ntid.x*ntid.y\n'
				'\tmov.u32 %rbtid,%rg5;");\n'								#threadID in a block;
			'\t//compute blockid in a grid\n'
			'\tasm volatile("mul.lo.u32	%rg6,%rnc1,%rnc2;\\n\\\n'	#rg6=nctaid.x*nctaid.y
				'\tmul.lo.u32	%rg7,%rg6,%rc3;\\n\\\n'					#rg7=ctaid.z*nctaid.x*nctaid.y
				'\tmul.lo.u32	%rg8,%rc2,%rnc1;\\n\\\n'				#rg8=ctaid.y*nctaid.x
				'\tadd.u32	%rg9,%rc1,%rg8;\\n\\\n'						#rg9=ctaid.x+ctaid.y*nctaid.x
				'\tadd.u32	%rg10,%rg9,%rg7;");\n'						#rg10=ctaid.x+ctaid.y*nctaid.x+ctaid.z*nctaid.x*nctaid.y\n'
			'\t//compute blocksize\n'
			'\tasm volatile("mul.lo.u32	%rg11,%rnt1,%rnt2;\\n\\\n'	#rg11=%ntid.x*%ntid.y;
				'\tmul.lo.u32	%rg12,%rg11,%rnt3;\\n\\\n'				#rg12=%ntid.x*%ntid.y*%ntid.z;
				'\tmul.lo.u32	%rg13,%rg10,%rg12;\\n\\\n'
				'\tadd.u32	%rgtid,%rg13,%rbtid;");\n'						#global threadID in a grid;
		)
		file_stream.write(
			'\tasm volatile(".reg .u64	%rdf<3>;\\n\\\n'			#parameter float data addr regs
				'\t.reg .u64	%rpf<3>;\\n\\\n'						#parameter float pointer addr regs
				'\t.reg .u64	%rdd<3>;\\n\\\n'						#parameter int data addr regs
				'\t.reg .u64	%rpd<3>;\\n\\\n'						#parameter int pointer addr regs
				'\t.reg .pred	%p_<10>;\\n\\\n'						#Predicate regs
				'\t.reg .f64	%f_<3>;\\n\\\n'							#float regs
				'\t.reg .s32	%d_<3>;\\n\\\n'							#int regs
				'\t.reg .u64	%offset;\\n\\\n'						#offset
				'\t.reg .u32	%loop;\\n\\\n'							#loop number
				'\t.reg .u32	%pass;\\n\\\n'							#pass
				'\t.reg .u64	%distance;\\n\\\n'							#pass
				'\t.reg .u32	%counter;");\n'							#loop counter
		)
		#file_stream.flush()

		tot_size=self.gridDim[0]*self.gridDim[1]*self.gridDim[2]*self.blockDim[0]*self.blockDim[1]*self.blockDim[2]
		file_stream.write(
			'\tasm volatile(".reg .u32	%rd<'+str(self.d_alu+self.d_mad+1)+'>;\\n\\\n'#int regs   Zhibin changes. +1 at the end
				'\t.reg .f64	%rf<'+str(self.f_alu+self.f_sfu+self.f_mad+1)+'>;\\n\\\n' #float regs   Zhibin changes. +1 at the end
				'\t.reg .b32	%rb<'+str(self.b_alu)+'>;\\n\\\n'						#byte regs
				'\t.reg .f64	%ropf3;\\n\\\n'											#3td float op regs
				'\t.reg .s32	%ropd3;\\n\\\n'											#3td int op regs
				'\t.reg .b32	%ropb<2>;\\n\\\n'										#byte regs
				'\tmov .b32	%ropb0,'+str(random.randint(10,1000))+';\\n\\\n'											#3td int op regs
				'\tmov .b32	%ropb1,'+str(random.randint(10,1000))+';\\n\\\n'											#3td int op regs
				'\tmov .u64	%distance,'+str(tot_size)+';\\n\\\n'											#3td int op regs
				'\tmov .s32	%ropd3,'+str(random.randint(10,10000))+';\\n\\\n'											#3td int op regs
				'\tmov .f64	%ropf3,'+str(random.uniform(1,100))+';");\n\n'											#3td float op regs
		)
		if self.shared_mem>0:
			self.declareSharedMem(file_stream)
		if self.const_mem>0:
			self.genConstMem(file_stream)
		file_stream.write(
		"\t//get the loop number\n"
		"\tasm volatile(\"ld.param.u32   %loop, [__cudaparm__Z6kernelPfS_S_PiS0_S0_i_loop];\");//loop\n\n"
		)
		#file_stream.flush();
		self.genParam(file_stream)
		#self.genLD(file_stream)
		for id in range(0,self.bbtype):	
			self.genInsn(file_stream,id)

		#self.genST(file_stream,'%rf'+str(self.n_f-1),'%rd'+str(self.n_d-1))

		#the last basic block
		file_stream.write(
		'\n\t//end basic block;\n'
		'\tasm volatile("$BB_LABEL'+str(self.bbtype)+':");\n'
		'\tasm volatile("exit;");\n'
		)
		file_stream.write('}\n')
		#file_stream.flush();

	######################################################################################
	# function genLD: used to load all the parameters
	# the values is moved to %f_0,%f_1,%d_0,%d_1
	######################################################################################
	def notComplete(self,n_falu,n_fsfu,n_fmad,n_dalu,n_dmad,n_balu,n_st_sm,n_ld_sm):
		return n_falu< self.f_alu or n_fmad<self.f_mad or n_fsfu<self.f_sfu or n_dalu<self.d_alu or n_dmad<self.d_mad or n_balu<self.b_alu or n_st_sm<self.st_shd or n_ld_sm<self.ld_shd;

	def notCompleteComputeInsn(self,n_falu,n_fsfu,n_fmad,n_dalu,n_dmad,n_balu):
		return n_falu< self.f_alu or n_fmad<self.f_mad or n_fsfu<self.f_sfu or n_dalu<self.d_alu or n_dmad<self.d_mad or n_balu<self.b_alu;
	def genInsn(self,file_stream,bbid=0):
		instruction=Intructions();
		#instruction mix counters
		n_falu=0
		n_fsfu=0
		n_fmad=0
		n_dalu=0
		n_dmad=0
		n_balu=0
		#shared memory counters
		n_st_sm=0
		n_ld_sm=0
		n_sm_d=0;#shared memory distance
		sm_flag=0;
		#constant memory counters
		n_const=0;
		self.genLD(file_stream)
		file_stream.write(
			'\tasm volatile("mov.u32	%counter,0;");\n'
			'\tasm volatile("$BB_LABEL'+str(bbid)+':");\n')
		#generate memory load
		#self.genLD(file_stream)
		# instruction mix
		file_stream.write('\t// instruction mix\n')
		file_stream.write('\tasm volatile("mov.u32 %pass,0;\\n\\\n')
		while (self.notCompleteComputeInsn(n_falu,n_fsfu,n_fmad,n_dalu,n_dmad,n_balu)):
			n=random.randint(0,6);
			#set shared memory load isntructions	
			if sm_flag==1 and n_st_sm>0 and n_ld_sm<self.ld_shd and (n_sm_d==self.sm_distance or self.sm_distance==0):
				self.genSharedMemLD(file_stream,'%rf'+str(random.randint(0,self.n_f-1)));
				n_ld_sm +=1
				n_sm_d=0
				sm_flag=0
				continue;
			#n==0: set float alu instructions
			if n==0 and n_falu<self.f_alu:
				instruction.setInsn(f_alu_list[random.randint(0,len(f_alu_list)-1)],'float','alu',str(self.n_f))
				n_falu+=1
				self.n_f+=1
				if(self.n_f <=self.reg_distance or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_f-self.reg_distance-1,self.n_f-self.reg_distance,self.n_f-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			#n==1:set float sfu instructions
			if n==1 and n_fsfu<self.f_sfu:
				instruction.setInsn(f_sfu_list[random.randint(0,len(f_sfu_list)-1)],'float','sfu',str(self.n_f))
				n_fsfu+=1
				self.n_f+=1
				if(self.n_f <=self.reg_distance or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_f-self.reg_distance-1,self.n_f-self.reg_distance,self.n_f-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			#n==2:set float mad instructions
			if n==2 and n_fmad<self.f_mad:
				instruction.setInsn(f_mad_list[random.randint(0,len(f_mad_list)-1)],'float','mad',str(self.n_f))
				n_fmad+=1
				self.n_f+=1
				if(self.n_f <=self.reg_distance  or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_f-self.reg_distance-1,self.n_f-self.reg_distance,self.n_f-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			#n==3:set int alu instructions
			if n==3 and n_dalu<self.d_alu:
				instruction.setInsn(d_alu_list[random.randint(0,len(d_alu_list)-1)],'int','alu',str(self.n_d))
				n_dalu+=1
				self.n_d+=1
				if(self.n_d <=self.reg_distance  or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_d-self.reg_distance-1,self.n_d-self.reg_distance,self.n_d-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			#n==4:set int mad instructions	
			if n==4 and n_dmad<self.d_mad:
				instruction.setInsn(d_mad_list[random.randint(0,len(d_mad_list)-1)],'int','mad',str(self.n_d))
				n_dmad+=1
				self.n_d+=1
				if(self.n_d <=self.reg_distance  or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_d-self.reg_distance-1,self.n_d-self.reg_distance,self.n_d-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			#n==5:set byte alu instructions
			if n==5 and n_balu<self.b_alu:
				instruction.setInsn(b_alu_list[random.randint(0,len(b_alu_list)-1)],'byte','alu',str(self.n_b))
				n_balu+=1
				self.n_b+=1
				if(self.n_b <=self.reg_distance  or self.reg_distance<1):
					file_stream.write('\t'+instruction.getInsn()+'\\n\\\n')
				else:
					file_stream.write('\t'+instruction.getInsnOP(self.n_b-self.reg_distance-1,self.n_b-self.reg_distance,self.n_b-self.reg_distance+1,self.reg_distance)+'\\n\\\n')
				if sm_flag==1:
					n_sm_d +=1;
			if n==6 and n_const<self.const_mem and self.n_f>0:
				self.genConstMemLD(file_stream,'%rf'+str(random.randint(0,self.n_f-1)));
				n_const+=1;
				if sm_flag==1:
					n_sm_d +=1;
			#n==6:set shared memory store instructions
			if self.n_f%2==0 and self.n_f>0 and n_st_sm<self.st_shd and sm_flag==0:
				self.genSharedMemST(file_stream,'%rf'+str(random.randint(0,self.n_f-1)));
				n_st_sm +=1
				sm_flag=1
				continue;

		file_stream.write('\t");\n')
		
		# generate memory Store 
		#self.genST(file_stream,'%rf'+str(self.f_alu+self.f_sfu+self.f_mad-1),'%rd'+str(self.d_alu+self.d_mad-1))
		file_stream.write('\tasm volatile("add.u32	%counter,%counter,1;\\n\\\n'
				'\tsetp.ge.u32	 %p_'+str(self.pcounter)+', %counter, %loop;\\n\\\n'
				'\t@!%p_'+str(self.pcounter)+'	bra	$BB_LABEL'+str(bbid)+';");\n')
		self.pcounter +=1
		self.genST(file_stream,'%rf'+str(self.f_alu+self.f_sfu+self.f_mad-1),'%rd'+str(self.d_alu+self.d_mad-1))
		#file_stream.flush();

	######################################################################################
	# function genParam: used to load all the parameters's address
	# the address of parameters is moved to %rdf0,%rdf1,%rdf2,%rdd0,%rdd1,%rdd2
	######################################################################################
	def genParam(self,file_stream):
		#genParameterAddr(file_stream)
		tmp=['0','1','2']
		tt=['d','f']
		file_stream.write('\tasm volatile("mul.wide.u32	%offset,%rgtid,4;");//get the address offset\n')
		for t in tt:
			for i in tmp:
				file_stream.write(
					'//'+t+i+' data\n'
					'\n\tasm volatile("ld.param.u64	%rp'+t+i+', [__cudaparm__Z6kernelPfS_S_PiS0_S0_i_'+t+i+'];\\n\\\n'
					'\tadd.u64	%rd'+t+i+',%rp'+t+i+',%offset;");\n'
				)
		file_stream.write('\t\n')

	######################################################################################
	# function genLD: used to load all the parameters
	# the values is moved to %f_0,%f_1,%d_0,%d_1
	######################################################################################
	def genLD(self,file_stream,d=0):
		tmp=['0','1']
		tt=['d','f']
		ss=''
		file_stream.write('//load the values of parameters\n')
		for t in tt:
			for i in tmp:
				ss='s32'		
				if t=='f':
					ss='f64'
				file_stream.write(
					'\tasm volatile("ld.global.'+ss+'	%'+t+'_'+i+',[%rd'+t+''+i+'+'+str(d)+'];");\n'
				)
		file_stream.write('\n\n')
		
		tot_size=self.gridDim[0]*self.gridDim[1]*self.gridDim[2]*self.blockDim[0]*self.blockDim[1]*self.blockDim[2]
		file_stream.write(
			'\tasm volatile("mul.wide.u32	%distance,'+str(tot_size)+',4;\\n\\\n'
			'\tadd.u64	%rdd0,%rdd0,%distance;\\n\\\n'
			'\tadd.u64	%rdd1,%rdd1,%distance;\\n\\\n'
			'\tadd.u64	%rdf0,%rdf0,%distance;\\n\\\n'
			'\tadd.u64	%rdf1,%rdf1,%distance;");\n'
			)
		#file_stream.flush();

	def genLD2(self,file_stream,d=0):
		tmp=['1']
		tt=['d','f']
		ss=''
		file_stream.write('//load the values of parameters\n')
		for t in tt:
			for i in tmp:
				ss='s32'		
				if t=='f':
					ss='f64'
				file_stream.write(
					'\tasm volatile("ld.global.'+ss+'	%'+t+'_'+i+',[%rd'+t+''+i+'+'+str(d)+'];");\n'
				)
		file_stream.write('\t\n')
	######################################################################################
	#	function genST: used to store all the computing results
	#	the values is stored from %f_2,%d_2 to the pointers f3,d3
	######################################################################################
	def genST(self,file_stream,f3,d3):
		file_stream.write('\n\tasm volatile("st.global.f64 [%rdf2+0],'+f3+';\\n\\\n'
					'\tst.global.s32 [%rdd2+0],'+d3+';");\n')
		file_stream.write(
			'\tasm volatile("add.u64	%rdf2,%rdf2,%distance;\\n\\\n'
			'\tadd.u64	%rdd2,%rdd2,%distance;");\n'
		)
	def generateCUDA(self):
		out=open(self.fname,'w')
		self.genHead(out)		#generate header 
		self.declareFloatP(out)	#declare Float pointer
		self.initFloatP(out)	#initialize the Float pointer
		self.declareIntP(out)	#declare Int Pointer
		self.initIntP(out)		#initialize the Int pointer
		self.callKernel(out)	#call the kernel
		self.printResult(out)	#print computing results
		self.genKernel(out)
		out.close()

if __name__ == '__main__':
	generator=Generator();
	generator.getParameter();
	generator.generateCUDA();
