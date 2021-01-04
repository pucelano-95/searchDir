"""
This script will search in a directory recursively.
Sources: https://github.com/Musta-Shr/LocalFoldersIdexing/blob/main/FileLookupV1_0.py

On 2 Jan. 2021 only supports text files.
@requirements: Python 2.5+
@author: Daniel Bueno Pacheco
"""

import os
import tkinter as tk
from tkinter import ttk, Button, filedialog, Label, Entry
from win32api import GetSystemMetrics
import magic
import threading


# Function that reads subfolders and add it to the main list
def ls_dir(path):
    dir_list = os.listdir(path)
    folder_paths = []
    for item in dir_list:
        item_path = path + "/" + item
        if os.path.isdir(item_path):
            folder_paths.append(item_path)
    return folder_paths


class Application(ttk.Frame):
    def __init__(self, main):
        super(Application, self).__init__()
        self.main_window = main
        self.width_screen = GetSystemMetrics(0)
        self.height_screen = GetSystemMetrics(1)
        self.main_window.geometry(str(self.width_screen) + "x" + str(self.height_screen))

        self.main_window.title("SearchDir - A search tool for searching the content of files")

        # Button browse directory
        self.buttonBrowse = Button(self.main_window, text="Browse directory",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.browse)
        self.buttonBrowse.place(relx=0.39, rely=0.08, relwidth=0.1, anchor="center")
        self.directory_search = Entry(self.main_window)
        self.directory_search.place(relx=0.55, rely=0.08, relwidth=0.2, anchor="center")

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
        self.contentLabel = Label(self.main_window, text="Content to search",
                                  font=("Verdana", round(self.width_screen / 160)))
        self.contentLabel.place(relx=0.39, rely=0.25, relwidth=0.3, anchor="center")
        self.content = Entry(self.main_window)
        self.content.place(relx=0.5, rely=0.25, relwidth=0.1, anchor="center")

        # Directory with output file.
        self.buttonOutput = Button(self.main_window, text="Output directory",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.outputDirectory)
        self.buttonOutput.place(relx=0.39, rely=0.30, relwidth=0.1, anchor="center")
        self.directory_output = Entry(self.main_window)
        self.directory_output.place(relx=0.5, rely=0.30, relwidth=0.1, anchor="center")

        # Error message
        self.message = Label(self.main_window, text="",
                             font=("Verdana", round(self.width_screen / 113)))
        self.message.place(relx=0.5, rely=0.5, anchor="center")

        # Button search
        self.buttonSearch = Button(self.main_window, text="Search",
                                   font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                   command=self.search)
        self.buttonSearch.place(relx=0.42, rely=0.4, relwidth=0.1, anchor="center")

        # Button cancel search
        self.buttonReset = Button(self.main_window, text="Reset",
                                  font=("Verdana", round(self.width_screen / 150)), relief="raised", bd=6,
                                  command=self.reset)
        self.buttonReset.place(relx=0.55, rely=0.4, relwidth=0.1, anchor="center")

    def browse(self):
        self.directory_search.insert(0, filedialog.askdirectory())
        return

    def outputDirectory(self):
        self.directory_output.insert(0, filedialog.askdirectory())
        return

    def search(self):
        self.block_interface()
        if self.checkContent():
            thread = threading.Thread(target=self.search_thread, args=())
            thread.start()
        else:
            self.show_message("Please specify the directory and the content to search.")
        return

    def search_thread(self):
        # Creating the seed list
        remaining_path = ls_dir(self.directory_search.get())
        if not remaining_path: # In case is empty
            remaining_path.append(self.directory_search.get())

        try:
            self.progressbar.start()
            # Looping through the list
            with open(self.directory_output.get() + "contentFound.txt", "wb") as output_file, \
                    open(self.directory_output.get() + "discardedFiles.txt", "wb") as discard_file:

                while len(remaining_path) > 0:
                    for folder in remaining_path:
                        dir_lst = os.listdir(folder)
                        for item in dir_lst:
                            full_item = folder + "/" + item
                            line_output = []
                            line_discard = []
                            if os.path.isfile(full_item):
                                type_of_text = magic.from_file(full_item, mime=True)
                                if type_of_text.find("text/") == 0:
                                    if self.extension.get() == "" or item.endswith(self.extension.get()):
                                        try:
                                            with open(full_item, "r") as f:
                                                i = 1
                                                line_found = False
                                                line_output.append("-------------------------------------------")
                                                line_output.append(full_item)
                                                for line in f:
                                                    if line.find(self.content.get()) != -1:
                                                        line_found = True
                                                        line_output.append("Line " + str(i) + " : " + line)
                                                    i = i + 1
                                                if not line_found:
                                                    line_output.append("Content not found")
                                                line_output.append("-------------------------------------------\n")

                                        except PermissionError:
                                            line_discard.append("-------------------------------------------")
                                            line_discard.append("File " + full_item +
                                                                " could not be read due to permissions.")
                                            line_discard.append("-------------------------------------------\n")
                                            line_output.clear()
                                        except UnicodeDecodeError:
                                            line_discard.append("-------------------------------------------")
                                            line_discard.append("File " + full_item +
                                                                " could not be read due to codification.")
                                            line_discard.append("-------------------------------------------\n")
                                            line_output.clear()
                                else:
                                    line_discard.append("-------------------------------------------")
                                    line_discard.append("File " + full_item + " is not a text file.")
                                    line_discard.append("-------------------------------------------\n")
                                    line_output.clear()
                            else:
                                try:
                                    new_items = ls_dir(folder)
                                    remaining_path.extend(new_items)
                                except PermissionError:
                                    line_discard.append("\n-------------------------------------------")
                                    line_discard.append("File " + full_item +
                                                        " could not be read due to permissions.")
                                    line_discard.append("-------------------------------------------")
                                    line_output.clear()


                            if line_discard:
                                discard_file.write("\n".join(line_discard).encode('utf-8'))
                                discard_file.flush()
                                line_discard.clear()
                            if line_output:
                                output_file.write("\n".join(line_output).encode('utf-8'))
                                output_file.flush()
                                line_output.clear()

                        if folder in remaining_path:
                            remaining_path.remove(folder)
        except IOError as err:
            print("Exception:", err, ". Error creating files contentFound.txt and discardedFiles.txt in",
                  self.directory_output)
        finally:
            output_file.close()
            discard_file.close()
            self.progressbar.stop()
            self.show_message("The search has been successful.")
        return

    def checkContent(self):
        if self.content.get() == "" or self.directory_search.get() == "":
            return False
        else:
            return True

    def show_message(self, message_output):
        if message_output != "":
            self.reset()
            self.message['text'] = message_output

    def reset(self):
        self.progressbar.stop()
        self.extension.config(state="normal")
        self.content.config(state="normal")
        self.directory_output.config(state="normal")
        self.directory_search.config(state="normal")
        self.message.config(state="normal")
        self.extension.delete(0, 'end')
        self.content.delete(0, 'end')
        self.directory_search.delete(0, 'end')
        self.directory_output.delete(0, 'end')
        self.message['text'] = ""
        self.buttonBrowse.config(state="normal")
        self.buttonSearch.config(state="normal")
        self.buttonOutput.config(state="normal")
        self.buttonReset.config(state="normal")
        return

    def block_interface(self):
        self.extension.config(state="disabled")
        self.content.config(state="disabled")
        self.directory_search.config(state="disabled")
        self.directory_output.config(state="disabled")
        self.message.config(state="disabled")
        self.buttonBrowse.config(state="disabled")
        self.buttonSearch.config(state="disabled")
        self.buttonOutput.config(state="disabled")
        self.buttonReset.config(state="disabled")
        return


if __name__ == "__main__":
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
