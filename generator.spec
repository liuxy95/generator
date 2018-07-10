#tournament_size 6
#demes_per_row 1
#demes_per_column 1
#deme_size 50
#migration_rate 0
#migration_delay 2
#migration_latency 1
#random_seed 3
#mutation_rate 0.05
#reproduction_rate 0.1
#elite_reproduction_rate 0.02
#crossover_rate 0.73
#uniform_crossover_rate 0.1
#structure_preserving_crossover_rate 0.0
#termination_fitness 240
#maximize_fitness 1

// Designing a Subway sub

problem_name = "test";

subrange 1..10 float_alu;
subrange 1..8 float_sfu;
subrange 1..6 float_mad;
subrange 1..8 int_alu;
subrange 1..6 int_mad;
subrange 1..4 byte_alu;
subrange 10..30	loop;
subrange 50..100 bbsize;
subrange 1..10	seed;
subrange 10..128 blockDim;
subrange 10..200 gridDim;
subrange 0..8 reg_distance;
subrange 0..8 shared_mem;
subrange 0..5 sm_distance; 
subrange 0..8 const_mem;

string_format = float_alu : float_sfu : float_mad : int_alu : int_mad : byte_alu : loop : bbsize : seed : blockDim : gridDim : reg_distance : sm_distance : shared_mem : const_mem;

//disallow(y>0 && y<48)

host_info {
        executable   = "./generator.pl";
		keep_files_from_failed_runs = 1;
        max_individuals_per_job = 1;
        max_parallel_individuals_per_job = 1;
        max_queued_jobs = 2;
        max_runtime = 1600; //seconds
}; //host_info
