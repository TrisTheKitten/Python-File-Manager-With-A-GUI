import os
import shutil
import hashlib
import tkinter as tk
from collections import defaultdict
from tqdm import tqdm
import time
import customtkinter as ctk
from tkinter import filedialog
import zipfile36 as zipfile
import webbrowser
from cryptography.fernet import Fernet
from tkinter import messagebox
import subprocess
import threading
import re
from difflib import SequenceMatcher
from datetime import datetime, timedelta

class PythonFileManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python File Manager")
        self.geometry("768x1000")
        self.resizable(False, True)

        self.directory = ctk.StringVar()
        self.output_directory = ctk.StringVar()
        self.organize_var = ctk.StringVar(value="None")
        self.sort_var = ctk.StringVar(value="None")
        self.delete_duplicates_var = ctk.BooleanVar(value=False)
        self.zip_files_var = ctk.BooleanVar(value=False)
        self.unzip_files_var = ctk.BooleanVar(value=False)
        self.delete_temp_files_var = ctk.BooleanVar(value=False)
        self.encrypt_files_var = ctk.BooleanVar(value=False)
        self.trim_ssd_var = ctk.BooleanVar(value=False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkFrame(self, bg_color="#edeff0", corner_radius=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=("#edeff0", "gray1"), height=50)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.app_label = ctk.CTkLabel(self.header_frame, text="File Manager", font=("San-Serif", 24, "bold"))
        self.app_label.grid(row=0, column=0, padx=20, pady=10)

        self.appearance_mode_switch = ctk.CTkSwitch(self.header_frame, text="Dark Mode", command=self.change_appearance_mode, fg_color="gray15", font=("San-Serif", 14, "bold"))
        self.appearance_mode_switch.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        self.updates_button = ctk.CTkButton(self.header_frame, text="Updates", command=self.open_github_releases, font=ctk.CTkFont(family="Sans-Serif", size=15, weight="bold"), fg_color="#0881a6", hover_color = "#ac5434")
        self.updates_button.grid(row=0, column=3, padx=(20, 10), pady=10, sticky="e")
        
        self.directory_frame = ctk.CTkFrame(self.main_frame, fg_color=("#d6d6d6", "gray15"), corner_radius=10)
        self.directory_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.directory_frame.grid_columnconfigure(0, weight=1)

        self.directory_label = ctk.CTkLabel(self.directory_frame, text="Input the Directory:", font=ctk.CTkFont(size=16))
        self.directory_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.directory_entry = ctk.CTkEntry(self.directory_frame, textvariable=self.directory, font=ctk.CTkFont(size=14))
        self.directory_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.browse_button = ctk.CTkButton(self.directory_frame, text="Browse", command=self.browse_directory, font=ctk.CTkFont(family="Sans-Serif", size=15, weight="bold"), fg_color="#0881a6", hover_color = "#ac5434")
        self.browse_button.grid(row=1, column=1, padx=(10, 20), pady=(0, 10))

        self.output_directory_frame = ctk.CTkFrame(self.main_frame, fg_color=("#d6d6d6", "gray15"), corner_radius=10)
        self.output_directory_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.output_directory_frame.grid_columnconfigure(0, weight=1)

        self.output_directory_label = ctk.CTkLabel(self.output_directory_frame, text="Output Directory:", font=ctk.CTkFont(size=16))
        self.output_directory_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.rename_button = ctk.CTkButton(self.directory_frame, text="Rename", command=self.rename_files, font=ctk.CTkFont(family="Sans-Serif", size=15, weight="bold"), fg_color="#0881a6", hover_color = "#ac5434")
        self.rename_button.grid(row=3, column=1, columnspan=1, padx=20, pady=(0, 10))
        
        self.output_directory_entry = ctk.CTkEntry(self.output_directory_frame, textvariable=self.output_directory, font=ctk.CTkFont(size=14))
        self.output_directory_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.output_browse_button = ctk.CTkButton(self.output_directory_frame, text="Browse", command=self.browse_output_directory, font=ctk.CTkFont(family="Sans-Serif", size=15, weight="bold"), fg_color="#0881a6", hover_color = "#ac5434")
        self.output_browse_button.grid(row=1, column=1, padx=(10, 20), pady=(0, 10))

        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color=("#d6d6d6", "gray15"), corner_radius=10)
        self.options_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.organize_label = ctk.CTkLabel(self.options_frame, text="Organize Files:", font=ctk.CTkFont(family="Sans-Serif", size=14, weight="bold"))
        self.organize_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.organize_combobox = ctk.CTkComboBox(self.options_frame, values=["None", "By Format", "By Name"], variable=self.organize_var, font=ctk.CTkFont(family="Sans-Serif", size=14, weight="bold"), corner_radius=5, fg_color="#d6d6d6")
        self.organize_combobox.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        self.sort_label = ctk.CTkLabel(self.options_frame, text="Sort Files:", font=ctk.CTkFont(family="Sans-Serif", size=14, weight="bold"))
        self.sort_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.sort_combobox = ctk.CTkComboBox(self.options_frame, values=["None", "By Size", "By Date"], variable=self.sort_var, font=ctk.CTkFont(family="Sans-Serif", size=14, weight="bold"), corner_radius=5, fg_color="#d6d6d6")
        self.sort_combobox.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.delete_duplicates_checkbox = ctk.CTkCheckBox(self.options_frame, text="Delete Duplicate Files", variable=self.delete_duplicates_var, font=ctk.CTkFont(size=14))
        self.delete_duplicates_checkbox.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.zip_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Zip Files", variable=self.zip_files_var, font=ctk.CTkFont(size=14))
        self.zip_files_checkbox.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.unzip_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Unzip Files(Only work with non-protected files)", variable=self.unzip_files_var, font=ctk.CTkFont(size=14))
        self.unzip_files_checkbox.grid(row=3, column=1, padx=20, pady=10, sticky="w")
            
        self.delete_temp_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Delete Temp & Prefetch Files", variable=self.delete_temp_files_var, font=ctk.CTkFont(size=14))
        self.delete_temp_files_checkbox.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.encrypt_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Encrypt Files(Experimental)", variable=self.encrypt_files_var, font=ctk.CTkFont(size=14))
        self.encrypt_files_checkbox.grid(row=4, column=1, padx=20, pady=10, sticky="w")
                        
        self.trim_ssd_checkbox = ctk.CTkCheckBox(self.options_frame, text="Trim SSD", variable=self.trim_ssd_var, font=ctk.CTkFont(size=14))
        self.trim_ssd_checkbox.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.file_listbox = tk.Listbox(self.directory_frame, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        self.file_details_frame = ctk.CTkFrame(self.directory_frame)
        self.file_details_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        self.file_details_label = ctk.CTkLabel(self.file_details_frame, text="", font=ctk.CTkFont(size=12))
        self.file_details_label.pack(padx=10, pady=10)

        self.process_button = ctk.CTkButton(self.main_frame, text="Process", command=self.process_files, font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), height=50, fg_color="#0881a6", hover_color = "#ac5434")
        self.process_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

        self.progress_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.progress_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="", font=ctk.CTkFont(size=14))
        self.progress_label.grid(row=0, column=0, padx=20, pady=10)

        self.version_label = ctk.CTkLabel(self.main_frame, text="Python File Manager V4", font=ctk.CTkFont(family="Sans-Serif", size=12, weight="bold"))
        self.version_label.grid(row=6, column=0, padx=(20, 0), pady=(0, 10), sticky="w")

        self.developer_label = ctk.CTkLabel(self.main_frame, text="Developed By Tris", font=ctk.CTkFont(family="Sans-Serif", size=12, weight="bold"))
        self.developer_label.grid(row=6, column=1, padx=(0, 20), pady=(0, 10), sticky="e")
        
        self.file_listbox.bind("<<ListboxSelect>>", self.show_file_details)
    
    def rename_files(self):
        selected_items = self.file_listbox.curselection()
        if not selected_items:
            ctk.CTkMessagebox(title="Error", message="No files or folders selected.")
            return

        directory = self.directory.get()
        if len(selected_items) == 1:
            # Single file or folder selected
            old_name = self.file_listbox.get(selected_items[0])
            new_name = ctk.CTkInputDialog(text="Enter new name:", title="Rename").get_input()
            if new_name:
                old_path = os.path.join(directory, old_name)
                name, extension = os.path.splitext(old_name)
                new_path = os.path.join(directory, f"{new_name}{extension}")
                os.rename(old_path, new_path)
                self.file_listbox.delete(selected_items[0])
                self.file_listbox.insert(selected_items[0], f"{new_name}{extension}")
        else:
            # Multiple files selected
            new_name = ctk.CTkInputDialog(text="Enter new name:", title="Batch Rename").get_input()
            if new_name:
                # Get the selected files and sort them
                selected_files = [self.file_listbox.get(index) for index in selected_items]
                selected_files.sort()

                # Rename the files with numbering
                for index, old_name in enumerate(selected_files, start=1):
                    old_path = os.path.join(directory, old_name)
                    name, extension = os.path.splitext(old_name)
                    new_file_name = f"{new_name} {index}{extension}"
                    new_path = os.path.join(directory, new_file_name)
                    os.rename(old_path, new_path)
                    self.file_listbox.delete(self.file_listbox.get(0, tk.END).index(old_name))
                    self.file_listbox.insert(tk.END, new_file_name)   
                     
    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select a Directory")
        if directory:
            if not os.path.exists(directory):
                messagebox.showerror("Error", "The selected directory does not exist.")
                return
            self.directory.set(directory)
            self.file_listbox.delete(0, tk.END)
            for item in os.listdir(directory):
                self.file_listbox.insert(tk.END, item)

    def browse_output_directory(self):
        output_directory = filedialog.askdirectory(title="Select Output Directory")
        if output_directory:
            if not os.path.exists(output_directory):
                messagebox.showerror("Error", "The selected output directory does not exist.")
                return
            self.output_directory.set(output_directory)
        
    def show_file_details(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index[0])
            file_path = os.path.join(self.directory.get(), selected_item)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                file_size_mb = file_size / (1024 * 1024)
                file_extension = os.path.splitext(selected_item)[1]
                file_details = f"Size: {file_size_mb:.2f} MB\nExtension: {file_extension}"
            elif os.path.isdir(file_path):
                file_details = "Directory"
            else:
                file_details = "No file selected."
        else:
            file_details = "No file selected."

        self.file_details_label.configure(text=file_details)
    
    def trim_ssd(self):
        try:
            os_drive = os.getenv("SystemDrive")
            if os_drive:
                subprocess.Popen(["defrag", os_drive, "/L"], creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                print("Unable to determine the Windows OS drive.")
        except Exception as e:
            print(f"Error trimming SSD: {e}")
        
    def delete_temp_files(self):
        temp_folders = [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
            os.path.expandvars(r"%WINDIR%\Prefetch")
        ]

        for folder in temp_folders:
            try:
                subprocess.Popen(["powershell", "-Command", f"Remove-Item -Path '{folder}' -Recurse -Force -ErrorAction SilentlyContinue"], creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                print(f"Error deleting files in {folder}: {e}")
                                
    def encrypt_file(self, file_path, password):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        with open(file_path + ".key", "wb") as key_file:
            key_file.write(key)

    def open_github_releases(self):
        webbrowser.open("https://github.com/TrisTheKitten/Python-File-Manager-With-A-GUI/releases")
        
    def zip_files(self, directory, output_directory):
        zip_file_path = os.path.join(output_directory, "zipped_files.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zip_file:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path != zip_file_path:  # Exclude the "zipped_files.zip" file
                        arcname = os.path.relpath(file_path, directory)
                        zip_file.write(file_path, arcname)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    arcname = os.path.relpath(dir_path, directory)
                    zip_file.write(dir_path, arcname)

    def unzip_files(self, directory, output_directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".zip"):
                    zip_path = os.path.join(root, file)
                    folder_name = os.path.splitext(file)[0]
                    folder_path = os.path.join(output_directory, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    with zipfile.ZipFile(zip_path, "r") as zip_file:
                        zip_file.extractall(folder_path)
                              
    def classify_files(self, directory):

        files = os.listdir(directory)
        file_groups = {}


        for file in files:
            file_name, file_ext = os.path.splitext(file)
            prefix_match = re.match(r'^(\w+)', file_name)
            if prefix_match:
                prefix = prefix_match.group(1)
                if prefix not in file_groups:
                    file_groups[prefix] = []
                file_groups[prefix].append(file)
            else:
                if 'others' not in file_groups:
                    file_groups['others'] = []
                file_groups['others'].append(file)

        for group_name, files in file_groups.items():
            folder_path = os.path.join(directory, group_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for file in files:
                file_path = os.path.join(directory, file)
                shutil.move(file_path, folder_path)
                print(f"Moved {file} to {folder_path}")
            if self.sort_by_date_var.get():
                self.classify_files_by_date(folder_path)

    def classify_files_by_date(self, folder_path):
        files = os.listdir(folder_path)
        date_ranges = [
            ('1 week ago', timedelta(days=7)),
            ('1 month ago', timedelta(days=30)),
            ('3 months ago', timedelta(days=90)),
            ('6 months ago', timedelta(days=180)),
            ('1 year ago', timedelta(days=365)),
            ('over 1 year', None)
        ]

        for file in files:
            file_path = os.path.join(folder_path, file)
            mod_time = os.path.getmtime(file_path)
            mod_datetime = datetime.fromtimestamp(mod_time)

            for sub_folder, date_range in date_ranges:
                if date_range is None or datetime.now() - mod_datetime <= date_range:
                    sub_folder_path = os.path.join(folder_path, sub_folder)
                    if not os.path.exists(sub_folder_path):
                        os.makedirs(sub_folder_path)
                    shutil.move(file_path, sub_folder_path)
                    print(f"Moved {file} to {sub_folder_path}")
                    break  
                                          
    def change_appearance_mode(self):
        if self.appearance_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.configure(bg_color="gray15")
        else:
            ctk.set_appearance_mode("light")
            self.configure(bg_color="#edeff0")
            
    def get_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def find_duplicates(self, directory):
        file_dict = defaultdict(list)
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_dict[self.get_md5(file_path)].append(file_path)
        return [v for v in file_dict.values() if len(v) > 1]

    def delete_duplicates(self, directory):
        duplicates = self.find_duplicates(directory)
        for duplicate_files in duplicates:
            for file_path in duplicate_files[1:]:
                os.remove(file_path)

    def move_files(self, source_dir, destination_dir, extensions):
        os.makedirs(destination_dir, exist_ok=True)

        files = [file for file in os.listdir(source_dir) if file.endswith(extensions)]
        for file in files:
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.move(source_path, destination_path)

    def get_folder_size(self, folder):
        total = 0
        for path, dirs, files in os.walk(folder):
            for f in files:
                fp = os.path.join(path, f)
                total += os.path.getsize(fp)
        return total / (1024 * 1024)

    def sort_files_and_folders(self, directory, output_directory):
        if not os.path.exists(directory):
            return

        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        folders = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

        for file in files:
            size_mb = os.path.getsize(file) / (1024 * 1024)
            if size_mb <= 100:
                os.makedirs(os.path.join(output_directory, "100MB files"), exist_ok=True)
                shutil.move(file, os.path.join(output_directory, "100MB files", os.path.basename(file)))
            elif size_mb <= 500:
                os.makedirs(os.path.join(output_directory, "500MB files"), exist_ok=True)
                shutil.move(file, os.path.join(output_directory, "500MB files", os.path.basename(file)))
            elif size_mb <= 1000:
                os.makedirs(os.path.join(output_directory, "1GB files"), exist_ok=True)
                shutil.move(file, os.path.join(output_directory, "1GB files", os.path.basename(file)))
            else:
                os.makedirs(os.path.join(output_directory, "over 1GB files"), exist_ok=True)
                shutil.move(file, os.path.join(output_directory, "over 1GB files", os.path.basename(file)))

        for folder in folders:
            size_mb = self.get_folder_size(folder)
            destination_dir = None
            if size_mb <= 100:
                destination_dir = os.path.join(output_directory, "100MB files")
            elif size_mb <= 500:
                destination_dir = os.path.join(output_directory, "500MB files")
            elif size_mb <= 1000:
                destination_dir = os.path.join(output_directory, "1GB files")
            else:
                destination_dir = os.path.join(output_directory, "over 1GB files")

            if destination_dir != folder:
                os.makedirs(destination_dir, exist_ok=True)
                shutil.move(folder, os.path.join(destination_dir, os.path.basename(folder)))

            if os.path.exists(folder):
                self.sort_files_and_folders(folder, os.path.join(output_directory, os.path.basename(folder)))
                
    def organize_files(self, directory, output_directory):
        file_types = {
            "pdf files": (".pdf", ".PDF", ".PDF_", ".pdf_"),
            "image files": (".jpeg", ".jpg", ".png", ".PNG", ".gif", ".tiff", ".bmp", ".webp", ".svg", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".raf", ".dng", ".arw", ".rw2", ".pef", ".x3f", ".kdc", ".mef", ".mrw", ".erf", ".mos", ".nrw", ".srw", ".rwl", ".dcr", ".ptx", ".raf", ".r3d", ".dng", ".crw", ".cr3", ".heic", ".heif", ".tif", ".tiff", ".jfif", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2", ".jxr", ".hdp", ".wdp", ".cur", ".ico", ".ase", ".aseprite", ".clip", ".cpt", ".heif", ".heic", ".kra", ".mdp", ".ora", ".pdn", ".reb", ".sai", ".tga", ".xcf", ".jpg-large", ".jpg-large_", ".jpg-large-"),
            "archive files": (".zip", ".rar", ".7z", ".tar", ".gz", ".tar.gz", ".xz"),
            "PPTX files": (".pptx", ".ppt", ".pptm", ".potx", ".potm", ".ppam", ".ppsx", ".ppsm", ".sldx", ".sldm"),
            "ipynb": (".ipynb"),
            "python": (".py", ".pyc", ".pyo", ".pyd", ".pyw", ".pyz", ".pywz", ".pyc", ".pyo", ".pyd", ".pywz", ".pyz"),
            "Excel files": (".xlsx", ".csv", ".xls", ".xlsm", ".xlt", ".xltx", ".xltm", ".xlsb", ".xlam", ".xlw", ".xlr", ".xlk", ".xla", ".xlm", ".xlw", ".xll", ".xl", ".xlam", ".xla", ".xltm", ".xlm", ".xltx", ".xlt", ".xlv", ".xlw", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt", ".xlv", ".xlr", ".xlk", ".xla", ".xlc", ".xlm", ".xll", ".xlv", ".xltm", ".xlt"),
            "Exe & Installers": (".exe", ".msi", ".bat", ".com", ".cmd", ".vbs", ".vbe", ".js", ".jse", ".ws", ".wsf", ".wsc", ".wsh", ".ps1", ".ps1xml", ".ps2", ".ps2xml", ".psc1", ".psc2", ".msh", ".msh1", ".msh2", ".mshxml", ".msh1xml", ".msh2xml", ".scf", ".lnk", ".inf", ".reg", ".dll", ".sys", ".cpl", ".ocx", ".ax", ".scr", ".crt", ".der", ".p7b", ".pfx", ".p12", ".p7r", ".spc", ".gpg", ".pgp", ".asc", ".cer", ".cert", ".key", ".pem", ".csr", ".crl", ".stl", ".sst", ".p7c", ".p7m", ".p7s", ".p8", ".p8e", ".p8r", ".p8s", ".p10", ".pki", ".pkipath", ".pfr", ".pko", ".p7", ".p7a", ".p7d", ".p7l", ".p7n", ".p7z", ".p7t", ".p7v", ".p7x", ".p7m", ".p7r", ".p7s", ".p8", ".p8e", ".p8r", ".p8s", ".p10", ".pki", ".pkipath", ".pfr", ".pko", ".p7", ".p7a", ".p7d", ".p7l", ".p7n", ".p7z", ".p7t", ".p7v", ".p7x", ".p7m", ".p7r", ".p7s", ".p8", ".p8e", ".p8r", ".p8s", ".p10", ".pki", ".pkipath", ".pfr", ".pko", ".p7", ".p7a", ".p7d", ".p7l", ".p7n", ".p7z", ".p7t", ".p7v", ".p7x", ".p"),
            "Document Files": (".docx", ".doc", ".docm", ".dotx", ".dotm", ".dot", ".docb", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot", ".uof", ".txt", ".rtf", ".pdf", ".html", ".htm", ".xml", ".xhtml", ".odt", ".ott", ".sxw", ".stw", ".uot"),
            "Java": (".java"),
            "Text Files": (".txt", ".log", ".md", ".json", ".yaml", ".yml", ".csv", ".tsv", ".xml", ".html", ".htm", ".css", ".js", ".php", ".cpp", ".cs", ".rb", ".pl", ".sql", ".swift", ".go", ".rs", ".kt", ".kts", ".scala", ".sh", ".ps1", ".bat", ".md", ".json"),
            "HTML files": (".html", ".htm", ".xhtml"),
            "CSS files": (".css"),
            "JavaScript files": (".js",),
            "XML files": (".xml",),
            "PHP files": (".php",),
            "C++ files": (".cpp",),
            "C# files": (".cs",),
            "Ruby files": (".rb",),
            "Perl files": (".pl",),
            "SQL files": (".sql",),
            "Swift files": (".swift",),
            "Go files": (".go",),
            "Rust files": (".rs",),
            "Kotlin files": (".kt", ".kts"),
            "Scala files": (".scala",),
            "Shell Script files": (".sh",),
            "PowerShell files": (".ps1",),
            "Batch files": (".bat",),
            "Markdown files": (".md", ".markdown"),
            "JSON files": (".json"),
            "Video files": (".mp4", ".mkv", ".webm", ".flv", ".vob", ".ogv", ".ogg", ".drc", ".gif", ".gifv", ".mng", ".avi", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".mpg", ".mpeg", ".mpe", ".mpv", ".mp2", ".m2v", ".m4v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".flv", ".f4v", ".f4p", ".f4a", ".f4b"),
        }

        for file_type, extensions in file_types.items():
            files = [file for file in os.listdir(directory) if file.endswith(extensions)]
            if files:
                destination_dir = os.path.join(output_directory, file_type)
                self.move_files(directory, destination_dir, extensions)


    def process_files(self):
        directory = self.directory.get()
        output_directory = self.output_directory.get()

        step = 0  # Initialize step variable
        total_steps = sum([
            self.trim_ssd_var.get(),
            self.delete_temp_files_var.get(),
            self.delete_duplicates_var.get(),
            self.organize_var.get() != "None",
            self.sort_var.get() != "None",
            self.zip_files_var.get(),
            self.unzip_files_var.get(),
            self.encrypt_files_var.get()
        ])

        progress_var = tk.DoubleVar()
        progress_bar = ctk.CTkProgressBar(self.progress_frame, variable=progress_var)
        progress_bar.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        if self.trim_ssd_var.get():
            self.trim_ssd()
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

        if self.delete_temp_files_var.get():
            self.delete_temp_files()
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

        if self.delete_duplicates_var.get():
            if not directory or not os.path.exists(directory):
                messagebox.showerror("Error", "Please select a valid input directory.")
                return
            self.delete_duplicates(directory)
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

        if self.organize_var.get() != "None" or self.sort_var.get() != "None" or self.zip_files_var.get() or self.unzip_files_var.get() or self.encrypt_files_var.get():
            if not directory or not os.path.exists(directory):
                messagebox.showerror("Error", "Please select a valid input directory.")
                return
            if not output_directory:
                messagebox.showerror("Error", "Please select a valid output directory.")
                return

        self.progress_label.configure(text="Processing...")
        self.update()

        total_steps = sum([
            self.organize_var.get() != "None",
            self.sort_var.get() != "None",
            self.delete_temp_files_var.get(),
            self.delete_duplicates_var.get(),
            self.zip_files_var.get(),
            self.unzip_files_var.get(),
            self.encrypt_files_var.get(),
            self.trim_ssd_var.get()
        ])

        progress_var = tk.DoubleVar()
        progress_bar = ctk.CTkProgressBar(self.progress_frame, variable=progress_var)
        progress_bar.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)  # Add this line

        self.progress_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        step = 0
        organize_option = self.organize_var.get()
        sort_option = self.sort_var.get()

        if organize_option != "None":
            if organize_option == "By Format":
                self.organize_files(directory, output_directory)
            elif organize_option == "By Name":
                self.classify_files(directory, output_directory)
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

            if sort_option != "None":
                if sort_option == "By Size":
                    self.sort_files_and_folders(output_directory, output_directory)
                elif sort_option == "By Date":
                    self.classify_files_by_date(output_directory)
                step += 1
                progress_var.set(step / total_steps)
                self.update_idletasks()
        else:
            if sort_option != "None":
                if sort_option == "By Size":
                    self.sort_files_and_folders(directory, output_directory)
                elif sort_option == "By Date":
                    self.classify_files_by_date(output_directory)
                step += 1
                progress_var.set(step / total_steps)
                self.update_idletasks()

        if self.zip_files_var.get():
            self.zip_files(directory, output_directory)
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

        if self.unzip_files_var.get():
            self.unzip_files(directory, output_directory)
            step += 1
            progress_var.set(step / total_steps)
            self.update_idletasks()

        if self.encrypt_files_var.get():
            password = ctk.CTkInputDialog(text="Enter password for encryption:", title="Encryption Password").get_input()
            if password:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.encrypt_file(file_path, password)
                step += 1
                progress_var.set(step / total_steps)
                self.update_idletasks()

        self.progress_label.configure(text="File Management completed.")
        tk.messagebox.showinfo("Success", "File Management completed successfully!")

if __name__ == "__main__":
    app = PythonFileManager()
    app.mainloop()
