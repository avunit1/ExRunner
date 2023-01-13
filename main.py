import tkinter as tk
from tkinter import filedialog, ttk
import random
import os
import glob
import time
import subprocess
import datetime

class AIT(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Avunit's Install Tool")
        self.geometry("700x900")
        self.configure(bg='white')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # big AIT text
        self.ait_text = tk.Label(self, text="AIT", font=("Helvetica", 32), bg='white')
        self.ait_text.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.ait_text.place(relx=0.5, rely=0.1, anchor="center")

        # smaller text
        self.small_text = tk.Label(self, text="Avunit's install tool", font=("Helvetica", 16), bg='white')
        self.small_text.grid(row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.small_text.place(relx=0.5, rely=0.2, anchor="center")

        # folder path entry and button
        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=50, bg='white', relief='solid', borderwidth=1)
        self.folder_entry.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.folder_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.folder_button = tk.Button(self, text="Select executables folder", command=self.select_folder)
        self.folder_button.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.folder_button.place(relx=0.5, rely=0.4, anchor="center")

        # output log text box
        self.output_log = tk.Text(self, height=20, width=85, relief='solid', borderwidth=1)
        self.output_log.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.output_log.place(relx=0.5, rely=0.6, anchor="center")
        self.output_log.config(state='normal')
        self.output_log.insert("1.0", "# Log goes here: \n", "grey_tag")
        self.output_log.config(state='disabled')
        self.output_log.tag_config("grey_tag", foreground='grey')

        # start install button
        self.start_button = tk.Button(self, text="Start Installing", command=self.start_install, width=20, height=2)
        self.start_button.grid(row=6, column=0, padx=20, pady=20, ipadx=0, ipady=0)
        self.start_button.place(relx=0.5, rely=0.95, y=-50, anchor="s")

        # progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=680)
        self.progress.grid(row=7, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.progress.place(relx=0.5, rely=0.95, y=20, anchor="s")

    def select_folder(self):
        folder = filedialog.askdirectory()
        self.folder_path.set(folder)

    def start_install(self):
        folder_path = self.folder_path.get()
        exe_files = glob.glob(os.path.join(folder_path, '*.exe'))
        self.output_log.config(state='normal')
        self.output_log.insert("end", "Scanning directory " + folder_path + "...\n")
        for file in exe_files:
            self.output_log.insert("end", "Found file: " + file + '\n')
        self.output_log.insert("end", "Scanning done. " + str(len(exe_files)) + " installers found. Starting in 5 seconds\n")
        self.output_log.config(state='disabled')
        self.countdown(5, exe_files)

    def countdown(self, count, exe_files):
        if count == 0:
            self.output_log.config(state='normal')
            self.output_log.insert("end", "Starting now.\n")
            self.output_log.config(state='disabled')
            self.run_installers(exe_files)
            return
        self.output_log.config(state='normal')
        self.output_log.insert("end", str(count) + "...\n")
        self.output_log.config(state='disabled')
        self.after(1000, self.countdown, count-1, exe_files)

    def run_installers(self, exe_files):
        for i, file in enumerate(exe_files):
            subprocess.run(file)
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.output_log.config(state='normal')
            self.output_log.insert("end", "Executable " + file + " ran at " + current_time + "\n")
            self.output_log.config(state='disabled')
            if i == len(exe_files) - 1:
                self.output_log.insert("end", "Done!\n")
                with open("log.txt", "w") as f:
                    f.write(self.output_log.get("1.0", "end"))

if __name__ == "__main__":
    app = AIT()
    app.mainloop()