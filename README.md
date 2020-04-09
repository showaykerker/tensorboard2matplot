# tensorboard2matplot
Python tool to convert multiple tensorflow events to matplot with shaded area as a representation of variance between different events in the same group.

The script searches tensorflow event files recursively under given path, combines them into pandas DataFrame, does calculations and plots the data into matplot.


## Requirement
* python3
	* tensorflow ( tested on version 1.15.2 )
	* matplotlib ( tested on version 3.1.1 )
	* pandas ( tested on version 0.25.1 )
	* numpy ( tested on version 1.17.4 )

## Usage
#### Grouping Events
Tensorboard `--logdir` allows to give an alias to folders, e.g. `--logdir=aliases:folder_path`. These aliases are used to name groups.
As a result, there will be # of filtered_tags subplots sharing x axis, each subplot contains # of groups of data lines that show moving average and variance (or min-max) of the group.

For example, there are 3 sets of hyperparameters named `set1`, `set2` and `set3` with folders `folder1`, `folder2` and `folder3` respectively. Each set runs 4 experiments with different random seed. These runs generate tensorflow events under the folder of given set.
```
root_path
├ folder1
│├ set1-run1
│├ set1-run2
│├ set1-run3
│└ set1-run4
├ folder2
│├ set2-run1
│├ set2-run2
│├ set2-run3
│└ set2-run4
└ folder3
　├ set3-run1
　├ set3-run2
　├ set3-run3
　└ set3-run4
```
With argument `--logdir=set1:folder1,set2:folder2,set3:folder3`, each runs with same set of hyperparameter are a group. The tool then calculates mean and variance (or min-max value) of runs under each group with respect to iterations and filtered tags.

#### DataFrame Interpolation
If there exists different frequency of data logging, some field might be empty. Under this situation, DataFrame interpolation is used.

Currently only `method` and `limit_direction` were given, if having any furthrer request, just add to the `interpolation_kwargs` in `main.py`
For further information, please refer to [this page](https://pandas.pydata.org/pandas-docs/version/0.25.1/reference/api/pandas.DataFrame.interpolate.html?highlight=interpolate).

#### Exception Handling
1. **DataLossError**: Sometimes the event file can be saving unexpectedly that causes  `tf.errors.DataLossError`, under this circumstances, the `event_loader` with give up the event file. Search `DataLossError` in `event_loader.py` for more information.

2. **KeyError**: This might happen when filtered tags are lost in some of the event. Most likely to happen when each events logged data with different name. That way, the `plotter` will give up logging the whole group. Search `KeyError` in `plotter.py` for more information.

## Example
* `python3 main.py --rootpath /path/to/simulations/ --logdir 0404:sim0404,0406:sim0406 --regex "train" --tags "performance" -y --use_min_max --save_data tmp --moving_average 0.9 --title performances`
![example1](https://github.com/showaykerker/tensorboard2matplot/blob/master/assets/example1.png)

* `python3 main.py --load_data tmp.pkl --moving_average 0.96 --title performances`
![example2](https://github.com/showaykerker/tensorboard2matplot/blob/master/assets/example2.png)

* `python3 main.py --rootpath /path/to/simulations/ --logdir mono:sim_mono,bino:sim_bino --regex "train" --tags "performance" --save_data example --moving_average 0.9 --title performances`
![example3](https://github.com/showaykerker/tensorboard2matplot/blob/master/assets/example3.png)

### Arguments
* Loading Events
	* **rootpath**: [str] This will append in front of logdirs.
	* **logdir**: [str] Same as tensorboarg commands for --logdir. The program will search for events file recurrently under the given directory.
	* **regex**: [str] Same as tensorboard runs filter, use regex to decide which event file(s) are being read.
	* **tags**: [str] Same as tensorboard tags filter, use regex to decide which tag(s) are being plot.
	* **downsample**: [int] Down sampling by loading only every N iters.
	* **interpolation_method**: [str] Interpolate method for `pandas.DataFrame.interpolate`.
	* **interpolation_direction**: [str] Interpolate direction for `pandas.DataFrame.interpolate`.

* Running Options
	* **title**: [str] Title on the plot.
	* **y**: Don't confirm loading events list after searching by regex. *[optional]*

* File IO
	* **save_data**: [str] If given, saving loaded data extract from events to this path.
	* **load_data**: [str] If given, loading data from this path reather than events.

* Plotting Configuration
	* **use_relative_time**: Use relative time reather than iters. Not functioning well. *[optional]*
	* **use_min_max**: Plot range using min max reather than using variance. *[optional]*
	* **moving_average**: [float] Smoothing data.


