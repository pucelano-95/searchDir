# import os
#
# path = "D:\\TEST\\SAFAL\\SG5.2MW-145CIIBMKII_MAKE(GF)_91m_DDBB(5.0MW_T91.4)\\"
# files_and_directories = os.listdir(path)
# # print (files_and_directories)
#
# try:
#     with open("D:\\TEST\\SAFAL\\foundTower.txt", "w") as sumFile:
#         for file in files_and_directories:
#             if file.endswith("xls"):
#                 sumFile.write(file + "\n")
#                 with open(path + file) as f:
#                     for line in f:
#                         if line.find("TOWER\tMY\t0") != -1:
#                             sumFile.write(line + "\n")
# except Exception as err:
#     print("Exception:", err)
"""
This script will search in a directory recursively.

On 2 Jan. 2021 only supports text files.
@requirements: Python 2.5+
@author: Daniel Bueno Pacheco
"""

import os
import tkinter as tk
from tkinter import ttk, Button, filedialog, Label, Entry
from win32api import GetSystemMetrics


class Application(ttk.Frame):
    def __init__(self, main):
        super(Application, self).__init__()
        self.directory = "./"
        self.main_window = main
        self.width_screen = GetSystemMetrics(0)
        self.height_screen = GetSystemMetrics(1)
        self.main_window.geometry(str(self.width_screen) + "x" + str(self.height_screen))

        self.main_window.title("SearchDir - A search tool for searching the content of files")

        # Button browse directory
        self.buttonBrowse = Button(self.main_window, text="Browse directory",
                                   font=("Verdana", round(self.width_screen / 77)), relief="raised", bd=6,
                                   command=self.browse)
        self.buttonBrowse.place(relx=0.5, rely=0.08, relwidth=0.3, anchor="center")

        # Create progress bar
        self.progressbar = ttk.Progressbar(self.main_window)
        self.progressbar.place(relx=0.5, rely=0.16, relwidth=0.3, anchor="center")

        # By default search in all files, but if we want we select the extension.
        self.extensionLabel = Label(self.main_window, text="Extension of files",
                                    font=("Verdana", round(self.width_screen / 160)))
        self.extensionLabel.place(relx=0.39, rely=0.20, relwidth=0.3, anchor="center")
        self.extension = Entry(self.main_window)
        self.extension.place(relx=0.5, rely=0.20, relwidth=0.1, anchor="center")

        # Content to search. This is mandatory.
        self.contentLabel = Label(self.main_window, text="Content of files",
                                  font=("Verdana", round(self.width_screen / 160)))
        self.contentLabel.place(relx=0.39, rely=0.25, relwidth=0.3, anchor="center")
        self.content = Entry(self.main_window)
        self.content.place(relx=0.5, rely=0.25, relwidth=0.1, anchor="center")

        # Directory with output file.
        self.buttonOutput = Button(self.main_window, text="Output directory",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.outputDirectory)
        self.buttonOutput.place(relx=0.39, rely=0.30, relwidth=0.1, anchor="center")
        self.output = Entry(self.main_window)
        self.output.place(relx=0.5, rely=0.30, relwidth=0.1, anchor="center")

        # Error message
        self.message = Label(self.main_window, text="",
                             font=("Verdana", round(self.width_screen/113)))
        self.message.place(relx=0.5, rely=0.5, anchor="center")

        # Button search
        self.buttonSearch = Button(self.main_window, text="Search",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.search)
        self.buttonSearch.place(relx=0.42, rely=0.4, relwidth=0.1, anchor="center")

        # Button cancel search
        self.buttonCancel = Button(self.main_window, text="Cancel search",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.reset)
        self.buttonCancel.place(relx=0.55, rely=0.4, relwidth=0.1, anchor="center")

    def browse(self):
        while True:
            self.directory = filedialog.askdirectory()
            if self.directory != "":
                break
        return

    def outputDirectory(self):
        self.output.insert(0, filedialog.askdirectory())
        return

    def search(self):
        if self.checkContent():
            dirlst = os.listdir(self.directory)
        else:
            self.show_message("Please write some content to search.")
        return

    def checkContent(self):
        return False

    def show_message(self, message_output):
        if message_output != "":
            # self.reset()
            self.message['text'] = message_output
        self.buttonBrowse.config(state="normal")

    def reset(self):
        pass


if __name__ == "__main__":
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
