import os, glob, re
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

        self.pathes = pathes.copy()
        self.aliases = aliases.copy()

        return pathes, aliases


    def load(self):
        pass
        
            

            

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



