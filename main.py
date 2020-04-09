import argparse
import pickle

import numpy as np

from event_loader import event_loader
from plotter import plotter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    ### Loading Events
    parser.add_argument("--rootpath", default="./", type=str, help='This will append in front of logdirs.')
    parser.add_argument("--logdir", default=".", type=str, help='Same as tensorboarg commands for --logdir.')
    parser.add_argument("--regex", default=".", type=str, help='Same as tensorboard runs filter, use regex to decide which event file(s) are being read.')
    parser.add_argument("--tags", default=".", type=str, help='Same as tensorboard tags filter, use regex to decide which tag(s) are being plot.')
    parser.add_argument("--downsample", default=100, type=int, help="Down sampling by loading only every N iters.")
    parser.add_argument("--interpolation_method", default="linear", type=str)
    parser.add_argument("--interpolation_direction", default="backward", type=str)
    ### 
    parser.add_argument("--title", default="title", type=str, help='Title on the plot.')
    parser.add_argument("-y", action="store_true", help="Don\'t confirm loading events list after searching by regex.")
    ### File IO
    parser.add_argument("--save_data", default="", type=str, help="If given, saving loaded data extract from events to this path.")
    parser.add_argument("--load_data", default="", type=str, help="If given, loading data from this path reather than events.")
    ### Plotting Configuration
    parser.add_argument("--use_relative_time", action="store_true", help="Use relative time reather than iters. Not functional well.")
    parser.add_argument("--use_min_max", action="store_true", help="Plot range using min max reather than using variance.")
    parser.add_argument("--moving_average", default=0., type=float, help="Smoothing data.")
    args = parser.parse_args()
    if args.rootpath[-1] != '/': args.rootpath += '/'
    args.moving_average = np.clip(args.moving_average, 0, 1)


    if args.load_data:
        with open(args.load_data, 'rb') as f:
            data = pickle.load(f)
        try:
            groups = data['groups']
        except KeyError:
            groups = data['teams']
        odict = data['odict']
        del data

    else:
        interpolation_kwargs = {
            "method": args.interpolation_method,
            "limit_direction": args.interpolation_direction
        }
        el = event_loader(args.rootpath, args.logdir)

        while True:
            groups, full_pathes, aliases = el.search(args.regex)
            print('\nFound events:')
                       
            for t_i, a_i in zip(groups, aliases): print('\t%s: %s' % (t_i, a_i))

            if not args.y:
                check = input('Correct? (Y/n) ')
                if check in ['n', 'N']:
                    args.regex = input('Input new regex rule: ')
                else: break
            else: break

        groups = el.groups
        odict = el.load(args.tags, args.downsample, interpolation_kwargs)
        data = {
            'groups': groups,
            'odict': odict
        }
        if args.save_data:
            with open('%s.pkl' % args.save_data, 'wb') as f:
                pickle.dump(data, f)

    """
    OrderedDict Structure
    {
        [ALIAS1]:{
            'start_time': [TIMESTAMP],
            'event_path': [FULL_PATH1],
            'data': [pandas DataFrame with tags as rows and step as columns],
            'groups': [TEAM_NAME]
        },
        [ALIAS2]:{
            'start_time': [TIMESTAMP],
            'event_path': [FULL_PATH2],
            'data': [pandas DataFrame with tags as rows and step as columns],
            'groups': [TEAM_NAME]
        },
        [ALIAS3]:{
            'start_time': [TIMESTAMP],
            'event_path': [FULL_PATH3],
            'data': [pandas DataFrame with tags as rows and step as columns],
            'groups': [TEAM_NAME]
        },
        ...
    }
    """

    pt = plotter(args.use_relative_time, args.use_min_max)
    pt.plot(odict, groups, suptitle=args.title, moving_avg=args.moving_average)