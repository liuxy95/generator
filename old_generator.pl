#!/usr/bin/perl

use Time::HiRes qw(gettimeofday);
#parse information passed in via stdin from SNAP
while(<STDIN>) {
    if(/^float_alu\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)		{ $float_alu1 = $1;} #if 
    if(/^float_sfu\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $float_sfu1 = $1;} #if
    if(/^float_mad\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $float_mad1 = $1;} #if
    if(/^int_alu\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $int_alu1 = $1;} #if
    if(/^int_mad\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $int_mad1 = $1;} #if
    if(/^byte_alu\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $byte_alu1 = $1;} #if
    if(/^loop\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $loop1 = $1;} #if
    if(/^bbsize\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $bbsize1 = $1;} #if
    if(/^seed\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $seed1 = $1;} #if
    if(/^blockDim\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $blockDim1 = $1;} #if
    if(/^gridDim\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $gridDim1 = $1;} #if
    if(/^reg_distance\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $reg_distance1 = $1;} #if
    if(/^sm_distance\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $sm_distance1 = $1;} #if
    if(/^shared_mem\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $shared_mem1 = $1;} #if
    if(/^const_mem\s+((-?\d*)\.?(\d*)(e[+-]\d+)?)/)     { $const_mem1 = $1;} #if
} #while


#Object is to maximize calories, penalizing heavily for exceeding max cost.
$fitness = compute_fitness($float_alu1,$float_sfu1,$float_mad1,$int_alu1,$int_mad1,$byte_alu1,$loop1,$bbsize1,$seed1,$blockDim1,$gridDim1,$reg_distance1,$sm_distance1,$shared_mem1,$const_mem1);


#print result for SNAP to grab
print STDOUT "\n".$fitness."\n\n";


#####################################################################
# compile the source file and generate the executable
# get result from simulator.
# ###################################################################
sub compute_fitness{
	my $float_alu,$float_sfu,$float_mad,$int_alu,$int_mad,$byte_alu,$loop,$bbsize,$seed,$blockDim,$gridDim,$reg_distance,$sm_distance,$shared_mem,$const_mem;
	($float_alu,$float_sfu,$float_mad,$int_alu,$int_mad,$byte_alu,$loop,$bbsize,$seed,$blockDim,$gridDim,$reg_distance,$sm_distance,$shared_mem,$const_mem)=@_;
	#open(FILE,">>log");
	my @time=($sec,$min,$hour,$day,$mon,$year)=localtime();
	my ($secss,$usec)=gettimeofday;
	$time[5]+=1900;
    my $exe;	
	$exe=join('-',reverse @time)."-".$secss."-".$usec."-".$$;
	$command="python py_generator.py -f ".$exe.".cu"." --float_alu=".$float_alu." --float_sfu=".$float_sfu." --float_mad=".$float_mad." --reg_distance=".$reg_distance." --int_alu=".$int_alu." --int_mad=".$int_mad." --byte_alu=".$byte_alu." --num_byte=1"." --loop=".$loop." --bbsize=".$bbsize." --bbtype=1"." --seed=".$seed." --blockDim='".$blockDim.",1,1'"." --gridDim='".$gridDim.",1,1'"." --sm_distance=".$sm_distance." --shared_mem=".$shared_mem." --const_mem=".$const_mem;
	$pid=fork;
	if($pid==0){
		exec($command);
		#print FILE "python generator.py:$command:$result\n";
	}
	waitpid($pid,0);
	$command="nvcc -o ".$exe." ".$exe.".cu"." -arch sm_12 --compiler-options -fno-strict-aliasing";
	$pid=fork;
	if($pid==0){
		exec($command);
		#print FILE "nvcc:$command:$result\n";
	}
	waitpid($pid,0);
	$command="./".$exe." > ".$exe.".txt";
	$pid=fork;
	if($pid==0){
		exec($command);
		#print FILE "nvcc:$command:$result\n";
	}
	waitpid($pid,0);
	#get power from output	
	open(FFF,$exe.".txt");
	my $power;
	while(<FFF>){
		chomp;
		if(/^gpu_tot_avg_power\s=\s(.*)/){ $power=$1;}
	}
	close(FFF);
	return $power;
	
}

#######################################################################
# fitness function
#######################################################################
sub compute{
	my $x1,$y1;
	#open(FILE,">>log");
	($x1,$y1)=@_;
	#print FILE "@_\n";
	#close(FILE);
	return compile($x1,$y1);
}
