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





class UmbertoRefreshCardListCommand(sublime_plugin.TextCommand):



    def run(self, edit):
        settings = sublime.load_settings('Umberto.sublime-settings')

        #print(sys.path)

        card_types = settings.get('card_types')
        if card_types is not None:
            type_list = list(card_types.keys())

        # Location of the current project.
        proj_dir = settings.get('current_project_directory')

        #self.pdf_refresh(proj_dir, type_list)
        self.store_code_list(proj_dir, type_list)
        # self.clean_up_aux_files(proj_dir, type_list)

    # def pdf_refresh(self, proj_dir, type_list):

    #     err_list = []
    #     total_file_cnt = 0
    #     typ_file_report = {}

    #     for typ in type_list:
    #         typ_file_cnt = 0
    #         folder = proj_dir + '/' + typ

    #         for file in os.listdir(folder):
    #             full_path = folder + '/' + file
    #             if file.endswith(".tex"):

    #                 total_file_cnt += 1
    #                 typ_file_cnt += 1

    #                 # pdf_path = file[0:-4] +'.pdf'
    #                 pdf_full_path = full_path[0:-4] + '.pdf'

    #                 tex_mod_time = os.path.getmtime(full_path)

    #                 try:
    #                     pdf_mod_time = os.path.getmtime(pdf_full_path)
    #                 except:
    #                     pdf_mod_time = 0

    #                 # if the pdf hasn't been updated
    #                 # since the tex file was updated
    #                 if pdf_mod_time < tex_mod_time:
    #                     get_cd = folder
    #                     os.chdir(get_cd)
    #                     build_tex = "pdflatex -halt-on-error " + file

    #                     process = sub.Popen(build_tex, shell=True)
    #                     process.wait()

    #                     try:
    #                         size = os.path.getsize(pdf_full_path)
    #                     except:
    #                         err_list.append(file)
    #                     else:
    #                         if size < 1000:
    #                          # less than 1 kb indicates corrupted pdf
    #                             err_list.append(file)
    #         typ_file_report[typ] = typ_file_cnt

    #     err_cnt = len(err_list)
    #     sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
    #     print("Refreshing PDFs complete.")
    #     print("A total of", total_file_cnt, "tex files were found, with the following breakdown by type:")
    #     print(typ_file_report)

    #     if err_cnt == 0:
    #         print("No build errors")
    #     else:
    #         print("A total of", err_cnt , "build errors occurred: check \n", err_list)


    def store_code_list(self, proj_dir, type_list):

        fname_list = [] #filenames
        fline_list = []     #first lines
        for typ in type_list:
            folder = proj_dir + '/' + typ

            for file in os.listdir(folder):
                if file.endswith(".tex"):
                    # file = file[3:-4] #extract author code
                    fname = folder + '/' +  file
                    short_fname = typ + '/' + file
                    firstline = open(fname).readline() #get first line of doc
                    firstline = firstline[1:-1] #trim off excess parts

                    # get the first word (code) from the first line
                    code = re.match('^[a-zA-Z0-9.\_]*', firstline).group(0)

                    # now get the first line minus the first word (the code)
                    try: 
                        trimmed_line = re.search('\s[\s\S]*', firstline).group(0)
                        trimmed_line = trimmed_line[1:] #remove initial space
                    except: #in case firstline is empty for some reason
                        trimmed_line = '0error'
                    

                    fname_list.append(code)
                    fline_list.append(trimmed_line)

        code_dict = dict(zip(fname_list, fline_list))

        storage_filename = proj_dir + "/lists/" + "code_list.json"
        with open(storage_filename, 'w') as storage:
            json.dump(code_dict, storage, sort_keys=True, indent=4 )

            print('Code list stored to ' + proj_dir)



















    def clean_up_aux_files(self, proj_dir, type_list):

        aux_file_ends = ['.aux', '.out', '.gz', '.log']

        for typ in type_list:
            folder = proj_dir + '/' + typ

            for file in os.listdir(folder):
                full_fname = folder + "/" + file

                for end in aux_file_ends:
                    if file.endswith(end):
                        os.remove(full_fname)
        print("Cleaned up .aux, .out and .log files")




