# open_card.py
# TGP 20171220 22.30

import json
import sublime
import sublime_plugin

class UmbertoOpenCardCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):
    def run(self, edit):
        settings = sublime.load_settings('Umberto.sublime-settings')

        card_types = settings.get('card_types')
        if card_types is not None:
            type_list = list(card_types.keys())

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

            file_name = self.code_list[jj]
            card_type = file_name[0:2]

            full_file_path = self.proj_dir + '/' + card_type + '/' + file_name + '.tex'
            self.view.window().open_file(full_file_path)

