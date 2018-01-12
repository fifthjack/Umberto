#new_project.py
# Set the current Umberto project in User settings

import os
import sublime
import sublime_plugin
import shutil




class UmbertoSetCurrentProjectCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):



    def on_done(self, j):
        curr_proj = self.project_list[j]
        curr_proj_dir = self.card_dir + '/' + curr_proj

        self.settings.set('current_project_directory', curr_proj_dir)
        sublime.save_settings('Umberto.sublime-settings')
        print('Current Project Directory has been changed to', curr_proj ,'.')


    def run(self, edit):

        self.settings = sublime.load_settings('Umberto.sublime-settings')

        card_dict = self.settings.get('card_directory')
        if card_dict is not None:
            self.card_dir = card_dict['directory']


        self.project_list = []
        for folder in os.listdir(self.card_dir):
            self.project_list.append(folder)


        self.view.window().show_quick_panel(self.project_list, self.on_done)










