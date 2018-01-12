#Command to refresh Umberto
# This involves two steps:
#  1. convert all modified tex to pdf
#  2. get list of card keys and titles

import sys
import os
import re
import json
import subprocess as sub
import sublime
import sublime_plugin





class UmbertoRefreshReadingListCommand(sublime_plugin.TextCommand):
    """Refreshes the list of documents in the Reading folder """
    def run(self, edit):
        settings = sublime.load_settings('Umberto.sublime-settings')

        # Location of the current project.
        self.proj_dir = settings.get('current_project_directory')

        # Location of the reading directory
        self.read_dir = settings.get('read_directory')
        #print(self.read_dir)

        #self.pdf_refresh(proj_dir, type_list)
        self.make_reading_list(self.proj_dir, self.read_dir)



    def make_reading_list(self, proj_dir, read_dir):

        fname_list = [] #filenames
        fpath_list = [] #file paths
        
        for root, dirs, files in os.walk(read_dir):
            for name in files:

                fname = name
                fname_list.append(fname)

                fpath = os.path.join(root, name)
                fpath = fpath.replace('\\', '/')
                fpath_list.append(fpath)

        read_dict = dict(zip(fname_list, fpath_list))

        storage_filename = proj_dir + "/lists/" + "reading_list.json"
        with open(storage_filename, 'w') as storage:
            json.dump(read_dict, storage, sort_keys=True, indent=4 )

            print('Reading list stored to ' + proj_dir + '/lists')

