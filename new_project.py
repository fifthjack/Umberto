#new_project.py
# Start a new Umberto index card system

import os
import sublime
import sublime_plugin
import shutil



class UmbertoNewProjectCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):
    
    def run(self, edit):

      # set the project directory in umberto settings
        settings = sublime.load_settings('Umberto.sublime-settings')

        card_types = settings.get('card_types')

        if card_types is not None:
            self.type_keys = list(card_types.keys())

        pkg_dict = settings.get('package_directory')
        if pkg_dict is not None:
            self.pkg_dir = pkg_dict['directory']

        card_dict = settings.get('card_directory')
        if card_dict is not None:
            self.card_dir = card_dict['directory']

        caption = 'Enter project name (no spaces):'
        initial_text = ''
        self.view.window().show_input_panel(caption, initial_text, self.on_done, None, None)




    def on_done(self, in_string):

        new_proj_dir = self.card_dir + '/' + in_string
        # create new folder
        if not os.path.exists(new_proj_dir):
            os.makedirs(new_proj_dir)

        for typ in self.type_keys:
            folder_path = new_proj_dir + '/' + typ
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move the relevant .sty file to the newly created typ folder
            try_path = self.pkg_dir + '/card_templates/' + typ + '_style.sty'
            if os.path.exists(try_path):
                sty_file_path = try_path
            else:
                sty_file_path = self.pkg_dir + '/card_templates/au_style.sty'
                #default is au

            shutil.copy(sty_file_path, folder_path)



