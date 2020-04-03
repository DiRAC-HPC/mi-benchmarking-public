# DiRAC Benchmark (Memory Intensive)

This repository contains data and analysis for benchmarking the [SWIFT](http://icc.dur.ac.uk/swift/) gravity and SPH solver on the [DiRAC](http://www.dirac.ac.uk) systems.

## SWIFT

### Obtaining the source code

To obtain a copy of the source code please see [https://gitlab.cosma.dur.ac.uk/swift/swiftsim](https://gitlab.cosma.dur.ac.uk/swift/swiftsim). For ease of comparison please use the tagged version 0.8.4 (commit fffd980b) on the master branch. 

In order to test compute performance only, the snapshot writing functions must be disabled by adding a return statement at the beginning of the function `engine_dump_snapshot` (line 4718 of `engine.c`). This is **NOT** in the tagged version and needs to be added by hand. All results presented here have this *feature*, and running without disabling the writing functions will provide results which are not directly comparable to the ones presented here.

### Compiling SWIFT

In general, to configure the SWIFT build use:

```
./autogen.sh
./configure <OPTIONS>
```

To see a list of possible configure options use `--help`. Once configured, compile the code with:

```
make -j
```

Specific configuration and compilation options for each of the benchmark platforms can be found in the relevant `data/` subdirectories of the benchmark directories for each system and compiler combination.

### Fetching input data

Navigate to desired example directory (e.g. `examples/EAGLE_low_z/EAGLE_12/`) and run:

```
./getIC.sh
```

### Running SWIFT

To run SWIFT, use

```
./run.sh
```

or add the command line within `run.sh` to a batch script.

Use the `--threads=<X>` to set the number of threads per process.

If using MPI, use the `swift_mpi` executable (called with the appropriate MPI launcher, e.g. `mpiexec`) instead of `swift`.

To set the number of steps to run the benchmark for use the `-n` option (here, we've used 2000 or 3000 steps). To see a list of command line options, run `swift --help`. 

### DiRAC Benchmarks

Parameter files (.yml) and command lines to run the examples are provided in the `data/` subdirectories for each individual benchmark. The actual data for the initial conditions is obtained using the `getIC.sh` script found in the source example subdirectories as described above. 

#### Single node benchmark

The single node benchmarks run here use the `examples/EAGLE_low_z/EAGLE_12/` example, replicated up to three times for weak scaling tests (the boxes are replicated in each of the three dimensions, so replicating 3 times results in a problem size 27x larger).

The benchmark has been run on the following systems:

| System | Node | Interconnect | Combinations |
|--------|------|--------------|--------------|
| DiRAC Memory Intensive (COSMA7) | 2x Intel Xeon Skylake Gold 5120, 512 GiB DDR4 | Mellanox EDR | Intel 2018; Intel MPI 2018 |
| DiRAC DIaC (Peta4-Skylake) | 2x Intel Xeon Skylake Gold 6142, min. 192 GiB DDR4 | Intel OPA | Intel 2018; Intel MPI 2018 | 
| DiRAC DIaL | 2x Intel Xeon Skylake Gold 6140, 192 GiB DDR4 | Mellanox EDR | Intel 2018; Intel MPI 2018 |

Output from benchmark runs can be found in the `results/` subdirectories of the specific `EAGLE_12` benchmark directories.

#### Multi-node benchmark

Strong scaling on multiple nodes use the `examples/EAGLE_low_z/EAGLE_25/` example. 

The benchmark has been run on the following systems:

| System | Node | Interconnect | Combinations |
|--------|------|--------------|--------------|
| DiRAC Memory Intensive (COSMA7) | 2x Intel Xeon Skylake Gold 5120, 512 GiB DDR4 | Mellanox EDR | Intel 2018; Intel MPI 2018 |
| DiRAC DIaC (Peta4-Skylake) | 2x Intel Xeon Skylake Gold 6142, min. 192 GiB DDR4 | Intel OPA | Intel 2018; Intel MPI 2018 | 

Output from benchmark runs can be found in the `results/` subdirectory of the `EAGLE_25_strong_scaling` directory.

#### Evaluating benchmark performance

Each run produces a `timesteps_X.txt` file, where `X` denotes the number of threads used. Examples of how to extract and process the performance data can be found in the [analysis/](analysis/) subdirectory.

## Further information

If you want further information on these benchmarks, please contact the DiRAC Helpdesk at: dirac-support@epcc.ed.ac.uk

