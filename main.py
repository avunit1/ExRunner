import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import os
import glob
import subprocess
import datetime
import hashlib
import sys
import shutil
import winreg
import random

def install_font(font_path):
    font_destination = "C:\\Windows\\Fonts\\"

    # Check if the font already exists in the destination folder
    font_name = os.path.basename(font_path)
    font_path_in_destination = os.path.join(font_destination, font_name)
    if os.path.exists(font_path_in_destination):
        print(f"{font_name} already exists in {font_destination}. Skipping installation.")
        return

    shutil.move(font_path, font_destination)

    # Register the font with Windows
    try:
        font_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(font_key, font_name, 0, winreg.REG_SZ, font_path_in_destination)
    except WindowsError:
        pass
    finally:
        winreg.CloseKey(font_key)

# Use the function to install a font
install_font("fonts/ComicCat.ttf")

def get_file_extension():
    return os.path.splitext(sys.argv[0])[1]

def get_hash_file_path():
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_extension = get_file_extension()
    if file_extension == '.py':
        hash_filename = "hash_py.md5"
    elif file_extension == '.exe':
        hash_filename = "hash_exe.md5"
    else:
        raise ValueError("Unsupported file type")
    
    return os.path.join(script_dir, 'hash', hash_filename)

def check_file_integrity():
    # Compute hash of the current file
    with open(sys.argv[0], 'rb') as f:
        current_file_hash = hashlib.sha256(f.read()).hexdigest()

    # Get the full path to the hash file
    hash_file_path = get_hash_file_path()

    # Compare the computed hash with the expected hash
    try:
        with open(hash_file_path, "r") as f:
            expected_hash = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Hash file not found: {hash_file_path}")

    if current_file_hash != expected_hash:
        # File has been tampered with
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error", "File has been tampered with.")
        root.destroy()
        sys.exit()

# Commented out the file integrity check
# check_file_integrity()

class AIT(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ExRunner 1.5")
        self.iconbitmap("images/new_icon.ico")
        self.geometry("700x670")
        self.configure(bg='#373A40')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.center()

        # banner
        banner_files = glob.glob("images/banner*.png")
        random_banner = random.choice(banner_files)
        self.icon = ImageTk.PhotoImage(Image.open(random_banner).resize((630, 353)))
        self.icon_label = tk.Label(self, image=self.icon, bg ='#373A40')
        self.icon_label.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.icon_label.place(relx=0.5, rely=0.13, y=17, anchor="center")

        # folder path entry and button
        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=112, bg='#373A40', fg='white', relief='solid', highlightbackground='#eeeeee', highlightthickness=2)
        self.folder_entry.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.grid_rowconfigure(2, minsize=2)
        self.folder_entry.place(relx=0.5, rely=0.3, y=67, anchor="center")
        self.folder_entry.configure(state='normal')
        self.folder_entry.delete(0, 'end')
        self.folder_entry.configure(background='#373A40', foreground='white')
        self.folder_entry.insert(0, "Selected directory will be shown here...")
        self.folder_entry.grid_propagate(False)
        self.folder_entry.config(justify='center')
        self.folder_entry.configure(bg='#373A40', fg='white')
        self.folder_entry.bind('<FocusIn>', lambda x: self.folder_entry.configure(foreground='white'))
        self.folder_entry.bind('<FocusOut>', lambda x: self.folder_entry.configure(foreground='white'))

        self.folder_button_frame = tk.Frame(self, bg='#eeeeee', bd=2)
        self.folder_button_frame.place(relx=0.7485, rely=0.4992, y=-105, anchor="center")

        self.folder_button = tk.Button(self.folder_button_frame, text="Select executables folder", command=self.select_folder, width=46, height=2, bg='#373A40', fg='white', relief='solid')
        self.folder_button.config(bd=0)
        self.folder_button.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.folder_button.place(relx=0.5, rely=0.4, y=-105, anchor="center")
        self.folder_button.configure(fg='#f6f6f6')
        self.folder_button.pack()

        # start install button
        self.start_button_frame = tk.Frame(self, bg='#eeeeee', bd=2)
        self.start_button_frame.place(relx=0.2515, rely=0.95, y=-387, anchor="s") # change relx=0.5 to relx=0.08

        self.start_button = tk.Button(self.start_button_frame, text="Start Installing", command=self.start_install, width=46, height=2, bg='#373A40', fg='white', relief='solid')
        self.start_button.config(bd=0)
        self.start_button.grid_forget()
        self.start_button.grid(row=6, column=0, padx=20, pady=20, ipadx=0, ipady=0)
        self.start_button.place(relx=0.5, rely=0.95, y=-387, anchor="s") 
        self.start_button.pack()

        # output log text box
        self.output_log = tk.Text(self, height=20, width=84, relief='solid', bg='#373A40', fg='white', highlightbackground='#eeeeee', highlightthickness=2)
        self.output_log.grid_forget()
        self.output_log.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.output_log.place(relx=0.5, rely=0.6, y=50, anchor="center")
        self.output_log.config(state='normal')
        self.output_log.insert("1.0", "# Log goes here: \n", "grey_tag")
        self.output_log.config(state='disabled')
        self.output_log.tag_config("grey_tag", foreground='white')

        # link button
        self.link_button = tk.Label(self, text="https://avunit1.github.io/", fg="#44a6c6", cursor="hand2", font=("Comic CAT", 12), bg="#373A40")
        self.link_button.grid(row=8, column=0, padx=20, pady=20, ipadx=0, ipady=0)
        self.link_button.place(relx=0.5, rely=1, y=-25, anchor="s")
        self.link_button.bind("<Button-1>", lambda e: webbrowser.open_new("https://avunit1.github.io/webpage-main/"))

        # copyright text
        self.copyright_text = tk.Label(self, text="©2024 avunit", font=("Comic CAT", 12), bg='#373A40', fg='white')
        self.copyright_text.grid(row=9, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.copyright_text.place(relx=0.5, rely=1, y=-5, anchor="s")

    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def visit_website(self, event):
        webbrowser.open_new(r"https://avunit1.github.io/webpage-main/")

    def select_folder(self):
    # Clear the output log text box first
        self.output_log.config(state='normal')
        self.output_log.delete("1.0", "end")
        self.output_log.config(state='disabled')

        # Open folder dialog and get the selected folder path
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            exe_files = self.scan_directory_for_executables(folder)
            if not exe_files:
                self.output_log.config(state='normal')
                self.output_log.insert("end", "No installers found, aborting.\n")
                self.output_log.see("end")
                self.output_log.config(state='disabled')
            else:
                self.output_log.config(state='normal')
                self.output_log.insert("end", "Scanning done. " + str(len(exe_files)) + " installers found.\n")
                self.output_log.see("end")
                self.output_log.config(state='disabled')
                for file in exe_files:
                    self.output_log.config(state='normal')
                    self.output_log.insert("end", "Found file: " + file + '\n')
                    self.output_log.see("end")
                    self.output_log.config(state='disabled')


    def scan_directory_for_executables(self, folder_path):
        exe_files = []
        self.output_log.config(state='normal')
        self.output_log.insert("end", "Scanning directory " + folder_path + "...\n")
        self.output_log.see("end")
        self.output_log.config(state='disabled')
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.exe') or file.endswith('.msi'):
                    exe_files.append(os.path.join(root, file))
        return exe_files

    def start_install(self):
        folder_path = self.folder_path.get()
        exe_files = self.scan_directory_for_executables(folder_path)
        if not exe_files:
            self.output_log.config(state='normal')
            self.output_log.insert("end", "No installers found, aborting.\n")
            self.output_log.see("end")
            self.output_log.config(state='disabled')
            return
        self.run_installers(exe_files)

    def run_installers(self, exe_files):
        for i, file in enumerate(exe_files):
            subprocess.run(file)
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.output_log.config(state='normal')
            self.output_log.insert("end", "Executable " + file + " ran at " + current_time + "\n")
            self.output_log.see("end")
            self.output_log.config(state='disabled')
            if i == len(exe_files) - 1:
                self.output_log.insert("end", "Done!\n")
                self.output_log.see("end")
                with open("log.txt", "w") as f:
                    f.write(self.output_log.get("1.0", "end"))

if __name__ == "__main__":
    app = AIT()
    app.mainloop()
