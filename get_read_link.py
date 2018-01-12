# SHOW CARD LIST
#


import os
import re
import json
import sublime
import sublime_plugin
import subprocess




class UmbertoGetReadLinkCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):

    def run(self, edit):

        settings = sublime.load_settings('Umberto.sublime-settings')

        # Location of the current project.

        self.proj_dir = settings.get('current_project_directory')
        self.read_dir = settings.get('read_directory')

        # load code_dict from json file
        dict_fname = self.proj_dir + '/lists/reading_list.json'
        with open(dict_fname) as json_data:
            read_dict = json.load(json_data)

        self.fname_list = list(read_dict.keys())
        self.fpath_list = list(read_dict.values())

        view_list = [[m, n] for m, n in zip(self.fname_list, self.fpath_list)]

        self.view.window().show_quick_panel(view_list, self.on_done)


    def on_done(self, jj):

        if jj < 0:
            return
        else:
            href_start = '\href{run:'
            href_mid = '}{'
            href_end = '}'

            fpath = self.fpath_list[jj]
            fname = self.fname_list[jj]

            # thanks to a quirk of LaTeX, certain characters are not permitted without a preceding backslash.
            # THe following code adds in backslashes when they're needed
            fname = re.sub('[\_\$]*', '', fname)

            insert_string = href_start + fpath + href_mid + fname + href_end
            
            self.view.run_command('insert', {'characters': insert_string})