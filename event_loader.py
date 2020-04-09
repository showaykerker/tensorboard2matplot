import os, glob, re
from collections import OrderedDict
import pandas as pd
import tensorflow as tf

class event_loader():
    def __init__(self, rootpath, logdir):
        self.rootpath = rootpath
        self.logdir = logdir

    def search(self, regex):
        regex = re.compile(regex)
        dirs = self.logdir.split(',')
        aliases = []
        pathes = []
        groups = []
        for title in dirs:
            if len(title.split(':')) == 1:
                if title[-1] != '/': title += '/'
                curr_alias = title
                curr_path = title
            else:
                splited = title.split(':')
                curr_alias = splited[0] + '/' if splited[0][-1] != '/' else ''
                curr_path = splited[1] + '/' if splited[1][-1] != '/' else ''

            path_list, simple_path = self._search_folder(self.rootpath+curr_path, curr_alias)

            for p, n in zip(path_list, simple_path):
                if regex.search(n) is not None: 
                    pathes.append(p)
                    aliases.append(n)
                    groups.append(curr_alias)

        self.pathes = pathes.copy()
        self.aliases = aliases.copy()
        self.groups = groups.copy()

        return groups, pathes, aliases


    def load(self, tags_regex, down_sample, interpolation_kwargs={"method": "linear", "limit_direction": "forward"}):
        regex = re.compile(tags_regex)
        odict = OrderedDict()
        
        removed_event_idx = []
        for i_event, (event_path, event_aliases, event_group) in enumerate(zip(self.pathes, self.aliases, self.groups)):
            print('Loading %s of group %s' % (event_aliases, event_group))
            odict[event_aliases] = {'start_time': None, 'data': {}, 'event_path': event_path, 'groups': event_group}
            try:
                for i, event in enumerate(tf.compat.v1.train.summary_iterator(event_path)):
                    if i == 0: odict[event_aliases]['start_time'] = event.wall_time
                    elif i % down_sample == 0:
                        for value in event.summary.value:
                            if regex.search(value.tag) is not None:
                                if event.step not in odict[event_aliases]['data'].keys():
                                    odict[event_aliases]['data'][event.step] = {}
                                    odict[event_aliases]['data'][event.step]['wall_time'] = event.wall_time
                                    odict[event_aliases]['data'][event.step]['relative'] = event.wall_time - odict[event_aliases]['start_time']
                                odict[event_aliases]['data'][event.step][value.tag] = value.simple_value

                odict[event_aliases]['data'] = pd.DataFrame.from_dict(odict[event_aliases]['data'], orient='index').interpolate(**interpolation_kwargs)

            except tf.errors.DataLossError as e:
                removed_event_idx.append(i_event)
                print('Error Occured. Give up loading events:', event_path)
                print('Error message:', e)

        for i in removed_event_idx[::-1]:
            del self.pathes[i], self.aliases[i], self.groups[i]
        
        return odict
            

    def _search_folder(self, path, alias):
        """
        Searching for event files under given path.
        
        Returns:
            paths: list of strings that are pathes of event files
        """
        path_list = []
        simple_path = []
        pathes = glob.glob(os.path.join(path+'*'))
        pathes.sort()
        for link in pathes:
            if os.path.isdir(link):
                folder_name = link.split('/')[-1] if link.split('/')[-1] != '' else link.split('/')[-2]
                inner_path_list, inner_simple_path = self._search_folder(link + '/' if link[-1] != '/' else '', alias + folder_name + '/' if folder_name[-1] != '/' else '')
                path_list += inner_path_list
                simple_path += inner_simple_path
            else:
                file_name = link.split('/')[-1]
                if file_name[:20] == "events.out.tfevents.":
                    path_list.append(link)
                    simple_path.append(alias+file_name)
        return path_list, simple_path



