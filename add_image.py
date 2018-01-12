#Command to refresh Umberto
# This involves two steps:
#  1. convert all modified tex to pdf
#  2. get list of card keys and titles

import sys
import os
import re
import math
import json
import subprocess as sub
import sublime
import sublime_plugin





class UmbertoAddImage(sublime_plugin.TextCommand):

    def run(self, edit):
        # Location of the current project.
        settings = sublime.load_settings('Umberto.sublime-settings')
        proj_dir = settings.get('current_project_directory')
        img_dir = proj_dir + "/images"

        # if not os.path.isdir("img_dir"):
        #     print('Image directory not found')
        #     img_dir = "C:"

        self.img_list = self.get_img_list(img_dir)

        self.view.window().show_quick_panel(self.img_list, self.on_done)



    def get_img_list(self, img_dir):

    	img_list = []
    	for file in os.listdir(img_dir):
    		img_list.append(file)
    	return img_list


    def on_done(self, jj):
        if jj < 0 or math.isnan(jj) == True:
            return
        else:
            img_name = self.img_list[jj]
            trunc_img_name = re.match('(.+)(?:\..+$)', img_name).group(1)
            print(trunc_img_name)

            fig_txt_start = r'\b' + 'egin{figure}\n\caption{Caption}\n\centering\n\includegraphics[width=0.7' + r'\t' + 'extwidth]{'
            fig_txt_two = '}\n\label{fig:'
            fig_txt_end = '}\n\end{figure}'

            insert_string = fig_txt_start + img_name+ fig_txt_two +  trunc_img_name + fig_txt_end

            self.view.run_command('insert', {'characters': insert_string})

