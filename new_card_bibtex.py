import sys
import os
import re
import sublime
import sublime_plugin
import shutil
import json







class UmbertoNewCardBibtexCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):

    def run(self, edit):
        settings = sublime.load_settings('Umberto.sublime-settings')

        self.pkg_dir = settings.get('package_directory')['directory']
        self.proj_dir = settings.get('current_project_directory')

        newview = sublime.active_window().new_file()
        self.view = newview

        caption = 'Enter the name of project bib file (e.g. mybib.bib)'       
        initial_text = ''
        newview.window().show_input_panel(caption, initial_text, self.input_done, None, None)

        

    def input_done(self, input_string):

        self.bib_dict = self.bib_to_dict(input_string)
        self.bib_list = self.bib_dict_to_list(self.bib_dict)
        self.view.window().show_quick_panel(self.bib_list, self.on_done)


    def on_done(self, j):
        if j == -1:
            return
        else:
            text = self.ob_from_bib(self.bib_list, self.bib_dict, j)

        if text is not None:
            self.view.run_command('insert_snippet', {'contents': text})

            # now save
            filename = self.key
            full_path = self.proj_dir + '/ob/ob.' + self.key + '.tex'
            self.view.retarget(full_path)
            self.view.run_command('save')





    def bib_to_dict(self, filename):

        # STEP 1 Get .bib file and import as a text string
        full_filename = self.proj_dir + '/' + filename
        with open(full_filename, 'r') as bibfile:
                bibtext = bibfile.read()

        # STEP 2.1 Split into individual entries
        bib_entries = re.split('\n@', bibtext)

        # remove first entry if it's a comment (starting with %)
        if re.match('%.+', bib_entries[0]) is not None:
            bib_entries = bib_entries[1:]  # remove @

        # remove last entry if it's a comment (starting Comment)
        if re.match('Comment.+', bib_entries[-1]) is not None:
            bib_entries = bib_entries[:-1]

        # print(bib_entries[2])
        # STEP 2.2 Extract useful information from the .bib string

        json_entries = []
        for j in range(len(bib_entries)):

            curr_entry = bib_entries[j]
            # print(curr_entry + 'ends')

            # ENTRY TYPE. entry type is the word after the @ symbol
            entry_type_full = re.match('.+{', curr_entry).group(0)
            entry_type = entry_type_full[:-1]

            curr_entry = curr_entry.replace(entry_type, '')
            # print(curr_entry)

            # BIBTEX KEY is the first word inside
            # curly braces {} after the init
            bibtex_key_full = re.match('^{.+', curr_entry).group(0)
            bibtex_key = bibtex_key_full[1:-1]
            # print(bibtex_key)

            new_key_string = '\n"bibtex_key": "' + bibtex_key + '"'

            curr_entry = curr_entry.replace(bibtex_key, new_key_string)

            # GENERAL CLEANUP
            # CONVERT BIB formatting to JSON
            curr_entry = curr_entry.replace('= {', ': "')
            curr_entry = curr_entry.replace('},\n', '",\n')
            # print(curr_entry)

            # ADD "" QUOTES to labels (they will become keys in JSON dict)
            key_list_raw = re.findall(r"(?:,\n)(.+)(?::\s)", curr_entry)
            key_list = ['"' + m.replace(' ', '') + '"' for m in key_list_raw]
            # print(key_list)
            for m in range(len(key_list)):
                old_str = key_list_raw[m]
                new_str = key_list[m]
                curr_entry = curr_entry.replace(old_str, new_str )
            # print(curr_entry)

            # remove new lines
            curr_entry = curr_entry.replace('\n' , '')

            # remove final comma
            curr_entry = curr_entry.replace(',}', '}' )

            # add entry_type into dict
            entry_type_string = '{"entry_type" : ' + '"' + entry_type + '",'
            curr_entry = curr_entry.replace('{', entry_type_string)

            json_entries.append(curr_entry)
            # print(curr_entry)
            




        # STEP 3 Convert string into dict

        bib_dict = {}
        for j in range(len(bib_entries)):
            entry_dict = json.loads(json_entries[j])
            entry_key = entry_dict['bibtex_key']
            bib_dict[entry_key] = entry_dict

        return bib_dict

    def bib_dict_to_list(self, bib_dict):
        bib_entries_list = []

        for key in bib_dict.keys():
            title = bib_dict[key]['title']
            bib_entry = [title, key]

            bib_entries_list.append(bib_entry)

        return bib_entries_list

    def ob_from_bib(self, bib_list, bib_dict, index):
        # first get bib data from dict
        list_entry = bib_list[index][1]
        self.key = re.match('^\w+', list_entry).group(0)

        # first, check if ob for this key already exists
        # otherwise it will be written over!

        # import code_list.json
        dict_fname = self.proj_dir + '/code_list.json'
        try:
            with open(dict_fname) as json_data:
                code_dict = json.load(json_data)
        except: code_dict = {}

        used_keys = list(code_dict.keys())
        new_full_key = 'ob.' + self.key
        if new_full_key in used_keys:
            print('A card for the bibtex key already exists')
            return

        bib_data = bib_dict[self.key]
        # print(bib_data)


        # RETRIEVE OB TEMPLATE
        tmpl_path = self.pkg_dir + '/card_templates/ob_tmpl.json'
        with open(tmpl_path, 'r') as tmpl_data:
            text = tmpl_data.read()
        
        # REPLACEMENTS

        full_code = 'ob.' + bib_data['bibtex_key']
        text = text.replace('$full_code$', full_code)

        title = bib_data['title']
        text = text.replace('$title$', title)

        new_sec_parts = ['author', 'year', 'date', 'journal']
        new_sec_string = r'\noindent\textbf{Reference Information}\newline' + '\n'

        for part in new_sec_parts:
            if part in bib_data:
                value = bib_data[part]
            else:
                value = 'unknown'
            part = part.title()
            if part == 'Author':
                part = 'Authors'
            value = value.title()
            full_value = part + ' : ' + value
            new_sec_string += full_value + r'\newline '

        new_sec_string += '\end{document}'

        text = text.replace('\end{document}', new_sec_string)
        
        return text










