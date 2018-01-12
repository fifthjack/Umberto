# SHOW CARD LIST
#


import os
import re
import json
import sublime
import sublime_plugin
import subprocess




class UmbertoGetCardLinkCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):

    def run(self, edit):

        settings = sublime.load_settings('Umberto.sublime-settings')

        # Location of the current project.

        self.proj_dir = settings.get('current_project_directory')

        # load code_dict from json file
        dict_fname = self.proj_dir + '/lists/code_list.json'
        with open(dict_fname) as json_data:
            code_dict = json.load(json_data)

        self.code_list = list(code_dict.keys())
        self.title_list = list(code_dict.values())

        view_list = [[m, n] for m, n in zip(self.title_list, self.code_list)]

        self.view.window().show_quick_panel(view_list, self.on_done)


    def on_done(self, jj):

        if jj < 0:
            return
        else:
            href_start = r'\href{run:../'
            href_mid = r'.pdf}{'
            href_end = r'}'

            code = self.code_list[jj]
            code_ref = str(code[0:2] + '/' + code)
            title = str(self.title_list[jj])

            # thanks to a quirk of LaTeX, certain characters are not permitted without a preceding backslash.
            # THe following code adds in backslashes when they're needed
            title = title.replace("_", "\_")

            insert_string = href_start + code_ref + href_mid + title + href_end
            
            self.view.run_command('insert', {'characters': insert_string})
            # Place cursor at the end of the line
            self.view.run_command("move_to", {"to": "eol"})