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





class UmbertoRefreshAllListsCommand(sublime_plugin.TextCommand):

    UmbertoRefreshCardList()
    UmbertoRefreshReadingList()

    # def run(self, edit):
    #     settings = sublime.load_settings('Umberto.sublime-settings')

    #     card_types = settings.get('card_types')
    #     if card_types is not None:
    #         type_list = list(card_types.keys())

    #     # Location of the current project.
    #     self.proj_dir = settings.get('current_project_directory')

    #     # Location of the reading directory
    #     self.read_dir = settings.get('read_directory')

    #     #self.pdf_refresh(proj_dir, type_list)
    #     self.store_code_list(self.proj_dir, type_list)
    #     self.make_reading_list(self.proj_dir, self.read_dir)

 
    # def store_code_list(self, proj_dir, type_list):

    #     fname_list = [] #filenames
    #     fline_list = []     #first lines
    #     for typ in type_list:
    #         folder = proj_dir + '/' + typ

    #         for file in os.listdir(folder):
    #             if file.endswith(".tex"):
    #                 # file = file[3:-4] #extract author code
    #                 fname = folder + '/' +  file
    #                 short_fname = typ + '/' + file
    #                 firstline = open(fname).readline() #get first line of doc
    #                 firstline = firstline[1:-1] #trim off excess parts

    #                 # get the first word (code) from the first line
    #                 code = re.match('^[a-zA-Z0-9.\_]*', firstline).group(0)

    #                 # now get the first line minus the first word (the code)
    #                 try: 
    #                     trimmed_line = re.search('\s[\s\S]*', firstline).group(0)
    #                     trimmed_line = trimmed_line[1:] #remove initial space
    #                 except: #in case firstline is empty for some reason
    #                     trimmed_line = '0error'
                    

    #                 fname_list.append(code)
    #                 fline_list.append(trimmed_line)

    #     code_dict = dict(zip(fname_list, fline_list))

    #     storage_filename = proj_dir + "/lists/" + "code_list.json"
    #     with open(storage_filename, 'w') as storage:
    #         json.dump(code_dict, storage, sort_keys=True, indent=4 )

    #         print('Code list stored to ' + proj_dir)

    # def make_reading_list(self, proj_dir, read_dir):

    #     fname_list = [] #filenames
    #     fpath_list = [] #file paths
        
    #     for root, dirs, files in os.walk(read_dir):
    #         for name in files:

    #             fname = name
    #             fname_list.append(fname)

    #             fpath = os.path.join(root, name)
    #             fpath = fpath.replace('\\', '/')
    #             fpath_list.append(fpath)

    #     read_dict = dict(zip(fname_list, fpath_list))

    #     storage_filename = proj_dir + "/lists/" + "reading_list.json"
    #     with open(storage_filename, 'w') as storage:
    #         json.dump(read_dict, storage, sort_keys=True, indent=4 )

    #         print('Reading list stored to ' + proj_dir + '/lists')




















    