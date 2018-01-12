# Create a new index card of a given type with title and file name

import sys
import os
import re
import shutil
import json
import sublime
import sublime_plugin
# current file location



# create new index card from input box
class NewCardInputCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):

    def run(self, edit):
        newview = sublime.active_window().new_file()

        self.view = newview
        print(sys.path)

        caption = 'type title'
        initial_text = ''

        newview.window().show_input_panel(caption, initial_text, self.on_done, None, None)

    def on_done(self, in_string):

        self.settings = sublime.load_settings('Umberto.sublime-settings')

        card_types = self.settings.get('card_types')
        if card_types is not None:
            type_keys = list(card_types.keys())
            type_values = list(card_types.values())

        try: self.proj_dir = self.settings.get('current_project_directory')
        except: self.proj_dir = "C:"

        self.pkg_dir = self.settings.get('package_directory')['directory']

        get_type = re.match("^\w+", in_string).group(0)
        get_title =  re.search("\s[\w\W]+$", in_string).group(0)

        # remove initial space in get_title, if present
        if get_title[0] == ' ':
            card_title = get_title[1:]
        else:
            card_title = get_title

        


        # get card type in two-letter format, in case it's given in long form
        # ie. author -> au
        if get_type in type_keys:
            card_type = get_type
        elif get_type in type_values:
            idx = [j for j, x in type_values if x == get_type]
            card_type = type_keys[idx]
        else:
            print('Card type not recognised. Using default (id)')

            card_type = 'id'

        # if card_type == 'au':
        #     code = self.make_au_code(card_title)
        # else:
        #     code = card_title

        # weird characters (e.g. underscores) in the file name will cause issues in LaTeX, so remove them
        card_title = card_title.replace("_","")

        #remove any weird characters from the code
        code = re.sub('[^A-Za-z0-9\_]+', '', card_title)
        if len(code) < 1:
            code = 'xxx'

        full_code = card_type + '.' + code

        # Retrieve index card template
        tmpl_path =  self.pkg_dir + '/card_templates/' + card_type + '_tmpl.json'
        with open(tmpl_path, 'r') as tmpl_data:
            text = tmpl_data.read()

        # Customise template to card details
        text = text.replace('$full_code$', full_code)
        text = text.replace('$title$', card_title)

        self.view.run_command('insert_snippet', {'contents': text})

        # now save
        full_path = self.proj_dir + '/' + card_type + '/' + card_type + '.' + code + '.tex'

        self.view.retarget(full_path)
        self.view.run_command('save')



    # def make_au_code(self, name):
    #     name = re.sub(r'[^a-zA-Z0-9-\s]', '', name)

    #     # first word
    #     first_word = re.match('^[\w-]+', name).group(0)
    #     last_word = re.search('[\w-]+$', name).group(0)

    #     initials = first_word[0] + last_word[0]

    #     for jj in range(100):
    #         if jj < 10:
    #             numstring = '0' + str(jj)
    #         else:
    #             numstring = str(jj)

    #         trycode = initials + numstring

    #         if self.is_code_already(trycode, self.proj_dir) is False:
    #             code = trycode
    #             break

    #     return code

    # def is_code_already(self, code, proj_dir):
    #     '''
    #     Check if the proposed code is already in use
    #     '''
    #     # 1 load json file
    #     dict_fname = self.proj_dir + '/code_list.json'
        
    #     try:
    #         with open(dict_fname) as json_data:
    #             code_dict = json.load(json_data)
    #     except: 
    #         return False

    #     code_list = list(code_dict.keys())

    #     full_code = 'au.' + code
    #     if full_code in code_list:
    #         return True
    #     else:
    #         return False














