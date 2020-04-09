# tensorboard2matplot
Tools to convert tensorboard to matplot with shaded area for variance or min-max between different events

## Requirement
* python3
	* tensorflow ( tested on version 1.15.2 )
	* matplotlib ( tested on version 3.1.1 )
	* pandas ( tested on version 0.25.1 )
	* numpy ( tested on version 1.17.4 )

## Usage
#### Grouping events
Tensorboard `--logdir` allows to give an alias to folders, e.g. `--logdir=aliases:folder_path`. These aliases are used to name groups.
As a result, there will be #filtered_tags subplots sharing x axis, each subplot contains #groups of data lines that show moving average and variance (or min-max).

#### DataFrame interpolation
Only `method` and `limit_direction` were given, if having any furthrer request, just add to the `interpolation_kwargs` in `main.py`
For further information, please refer to [this page](https://pandas.pydata.org/pandas-docs/version/0.25.1/reference/api/pandas.DataFrame.interpolate.html?highlight=interpolate).


## Example
* `python3 main.py --rootpath /path/to/simulations/ --logdir 0404:sim0404,0406:sim0406 --regex "train" --tags "performance" -y --use_min_max --save_data tmp --moving_average 0.9 --title performances`
![example1](https://github.com/showaykerker/tensorboard2matplot/blob/master/assets/example1.png)

* `python3 main.py --rootpath /path/to/simulations/ --logdir 0404:sim0404,0406:sim0406 --regex --tags "performance" --load_data tmp.pkl --moving_average 0.96 --title performances`
![example2](https://github.com/showaykerker/tensorboard2matplot/blob/master/assets/example2.png)

## Arguments
``` python
### Loading Events
parser.add_argument("--rootpath", default="./", type=str, 'This will append in front of logdirs.')
parser.add_argument("--logdir", default=".", type=str, 'Same as tensorboarg commands for --logdir.')
parser.add_argument("--regex", default=".", type=str, 'Same as tensorboard runs filter, use regex to decide which event file(s) are being read.')
parser.add_argument("--tags", default=".", type=str, 'Same as tensorboard tags filter, use regex to decide which tag(s) are being plot.')
parser.add_argument("--downsample", default=100, type=int, help="Down sampling by loading only every N iters.")
parser.add_argument("--interpolation_method", default="linear", type=str)
parser.add_argument("--interpolation_direction", default="backward", type=str)
### 
parser.add_argument("--title", default="title", type=str, 'Title on the plot.')
parser.add_argument("-y", action="store_true", help="Don\'t confirm loading events list after searching by regex.")
### File IO
parser.add_argument("--save_data", default="", type=str, help="If given, saving loaded data extract from events to this path.")
parser.add_argument("--load_data", default="", type=str, help="If given, loading data from this path reather than events.")
### Plotting Configuration
parser.add_argument("--use_relative_time", action="store_true", help="Use relative time reather than iters. Not functional well.")
parser.add_argument("--use_min_max", action="store_true", help="Plot range using min max reather than using variance.")
parser.add_argument("--moving_average", default=0., type=float, help="Smoothing data.")
```
