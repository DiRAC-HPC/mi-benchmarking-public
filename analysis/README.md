To generate scaling plots from the timesteps files found in the data subdirectory run the plotting scripts followed by a list of directories with the suffix `timesteps_` and a list of strings corresponding to the titles for the legend. For example:

```
python plot_weak_scaling_results.py ../results/cosma7/single-node/timesteps_ ../results/csd3/single-node/weak_scaling/timesteps_ "COSMA7" "CSD3"
```

To generate strong scaling results use `plot_strong_scaling_results.py` in a similar fashion.

The strong scaling plots by default compute results with respect to the number of threads. To compute values on a per node basis uncomment line 381 in `plot_strong_scaling_results.py`.
