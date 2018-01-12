# SHOW CARD LIST
#


import os
import re
import json
import sublime
import sublime_plugin
import subprocess




class UmbertoGetRecipCardLinkCommand(sublime_plugin.TextCommand, sublime_plugin.WindowCommand):

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
            href_start = '\href{run:../'
            href_mid = '.pdf}{'
            href_end = '}'

            code = self.code_list[jj]
            code_ref = code[0:2] + '/' + code
            title = self.title_list[jj]

            
             # thanks to a quirk of LaTeX, certain characters are not permitted without a preceding backslash.
            # THe following code adds in backslashes when they're needed
            title = title.replace("_", "\_")


            insert_string = href_start + code_ref + href_mid + title + href_end
            
            self.view.run_command('insert', {'characters': insert_string})
            self.see_also_link(code, title)

    def see_also_link(self, code, title):
        '''
        Generate a reciprocal link in a "See Also" section
        at the bottom of the index card
        '''
        # INFO ABOUT CURRENT FILE = THISFILE
                # get path and file name of the current file
        current_file_code = self.view.window().extract_variables()['file_base_name']
        typ_thisfile = current_file_code[0:2]
        current_file_name = self.view.window().extract_variables()['file_name']

        # # COMPILE CURRENT FILE
        # get_cd = self.proj_dir + '/' + typ_thisfile 
        # os.chdir(get_cd)
        # build_tex = "pdflatex -halt-on-error " + current_file_name

        # process = subprocess.Popen(build_tex, shell=True)
        # process.wait()
        
        # GET current file title
        spatt = '\\lhead{.*}'
        curr_file_contents = self.view.substr(sublime.Region(0, self.view.size()))
        try: 
            curr_title = re.search(spatt, curr_file_contents).group(0)

        except: curr_title = 'Title'

        curr_title = curr_title.replace('lhead{', '')
        curr_title = curr_title.replace('}', '')

        # open the file specified by code = THATFILE
        typ_thatfile = code[0:2]
        thatfile = self.proj_dir + '/' + typ_thatfile + '/' + code + '.tex'
        with open(thatfile, 'r') as thatfile_data:
            text = thatfile_data.read()

        # search tex for \noindent\textbf{See Also}\newline
        # if it's there, append new reciprocal link
        # if it's not there, add this See Also section and 
        # append new recip link

        # USEFUL STRINGS
        
        code_ref = typ_thisfile + '/' + current_file_code

        sa_title = r'\noindent\textbf{See Also}\newline' + '\n'
        end_doc = '\end{document}'

        href_start = '\href{run:../'
        href_mid = '.pdf}{'
        href_end = r'}\newline' + '\n'


        insert_string = href_start + code_ref + href_mid + curr_title + href_end
        new_sec = insert_string  + '\n'
        

        if sa_title in text:
            new_end_doc = new_sec + end_doc
            text = text.replace(end_doc, new_end_doc)
        else:
            new_end_doc = sa_title + new_sec + end_doc
            text = text.replace(end_doc, new_end_doc)

        with open(thatfile, 'w') as f:
            f.write(text)

        # # Recompile
        # get_cd = self.proj_dir + '/' + typ_thatfile 
        # os.chdir(get_cd)
        # build_tex = "pdflatex -halt-on-error " + code + '.tex'

        # process = subprocess.Popen(build_tex, shell=True)
        # process.wait()