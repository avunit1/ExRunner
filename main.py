import tkinter as tk
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

def check_file_integrity():
    # Compute hash of the current file
    with open(sys.argv[0], 'rb') as f:
        current_file_hash = hashlib.sha256(f.read()).hexdigest()

    # Compare the computed hash with the expected hash
    with open("hash/hash.md5", "r") as f:
        expected_hash = f.read()

    if current_file_hash != expected_hash:
        # File has been tampered with
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error", "File has been tampered with.")
        root.destroy()
        sys.exit()

# Run the check_file_integrity function at the start
check_file_integrity()

class AIT(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ExRunner")
        self.iconbitmap("images/icon.ico")
        self.geometry("700x800")
        self.configure(bg='#1e1e1e')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.center()

        # banner
        self.icon = ImageTk.PhotoImage(Image.open("images/banner.png").resize((500, 280)))
        self.icon_label = tk.Label(self, image=self.icon, bg ='#1e1e1e')
        self.icon_label.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.icon_label.place(relx=0.5, rely=0.1, y=63, anchor="center")

        # folder path entry and button
        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=50, bg='#323232', fg='#f6f6f6', relief='solid', borderwidth=1)
        self.folder_entry.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.folder_entry.place(relx=0.5, rely=0.3, y=107, anchor="center")
        self.folder_entry.configure(state='normal')
        self.folder_entry.delete(0, 'end')
        self.folder_entry.configure(background='#323232', foreground='white')
        self.folder_entry.insert(0, "Selected directory will be shown here...")
        self.folder_entry.config(justify='center')
        self.folder_entry.configure(bg='#323232', fg='#f6f6f6')
        self.folder_entry.bind('<FocusIn>', lambda x: self.folder_entry.configure(foreground='white'))
        self.folder_entry.bind('<FocusOut>', lambda x: self.folder_entry.configure(foreground='white'))

        self.folder_button = tk.Button(self, text="Select executables folder", command=self.select_folder, width=20, height=2, bg='#323232', fg='#f6f6f6')
        self.folder_button.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.folder_button.place(relx=0.5, rely=0.4, y=-13, anchor="center")
        self.folder_button.configure(fg='#f6f6f6')

        # start install button
        self.start_button = tk.Button(self, text="Start Installing", command=self.start_install, width=20, height=2, bg='#323232', fg='#f6f6f6')
        self.start_button.grid_forget()
        self.start_button.grid(row=6, column=0, padx=20, pady=20, ipadx=0, ipady=0)
        self.start_button.place(relx=0.5, rely=0.95, y=-353, anchor="s")
        self.start_button.configure(fg='#f6f6f6')

        self.bottom_frame = tk.Frame(self, bg='white')
        self.bottom_frame.place(relx=0.5, rely=1, y=-20, anchor="s")

        # output log text box
        self.output_log = tk.Text(self, height=20, width=84, relief='solid', borderwidth=1, bg='#323232', fg='#f6f6f6')
        self.output_log.grid_forget()
        self.output_log.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.output_log.place(relx=0.5, rely=0.6, y=100, anchor="center")
        self.output_log.config(state='normal')
        self.output_log.insert("1.0", "# Log goes here: \n", "grey_tag")
        self.output_log.config(state='disabled')
        self.output_log.tag_config("grey_tag", foreground='#c5c5c5')

        # link button
        self.link_button = tk.Label(self, text="https://avunit.tk/", fg="#44a6c6", cursor="hand2", font=("Comic CAT", 12), bg="#1e1e1e")
        self.link_button.grid(row=8, column=0, padx=20, pady=20, ipadx=0, ipady=0)
        self.link_button.place(relx=0.5, rely=1, y=-25, anchor="s")
        self.link_button.bind("<Button-1>", lambda e: webbrowser.open_new("https://avunit.tk/"))

        # copyright text
        self.copyright_text = tk.Label(self, text="©2023 avunit", font=("Comic CAT", 12), bg='#1e1e1e', fg='white')
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
        webbrowser.open_new(r"https://avunit.tk/")

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