import argparse
from event_loader import event_loader


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--rootpath", default="./", type=str)
    parser.add_argument("--logdir", default=".", type=str)
    parser.add_argument("--regex", default=".", type=str)
    parser.add_argument("--tags", default=".", type=str)
    parser.add_argument("-y", action="store_true")
    args = parser.parse_args()
    if args.rootpath[-1] != '/': args.rootpath += '/'

    el = event_loader(args.rootpath, args.logdir)

    while True:
        full_pathes, aliases = el.search(args.regex)
        print('\nFound events:')
        for a_i in aliases: print('\t%s' % a_i)
        if not args.y:
            check = input('Correct? (Y/n) ')
            if check in ['n', 'N']:
                args.regex = input('Input new regex rule: ')
            else: break
        else: break


