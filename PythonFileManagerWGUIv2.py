import os
import shutil
import hashlib
from collections import defaultdict
from tqdm import tqdm
import time
import customtkinter as ctk

class PythonFileManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python File Manager")
        self.geometry("500x450")
        self.resizable(False, False)

        self.directory = ctk.StringVar()
        self.delete_duplicates_var = ctk.BooleanVar(value=True)
        self.sort_files_var = ctk.BooleanVar(value=True)
        self.move_files_var = ctk.BooleanVar(value=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        self.directory_label = ctk.CTkLabel(self.main_frame, text="Input the Directory:", font=ctk.CTkFont(size=14))
        self.directory_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")

        self.directory_entry = ctk.CTkEntry(self.main_frame, textvariable=self.directory, width=400, font=ctk.CTkFont(size=14))
        self.directory_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 20))

        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.delete_duplicates_checkbox = ctk.CTkCheckBox(self.options_frame, text="Delete Duplicate Files", variable=self.delete_duplicates_var, font=ctk.CTkFont(size=14))
        self.delete_duplicates_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.sort_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Sort Files Based on Size", variable=self.sort_files_var, font=ctk.CTkFont(size=14))
        self.sort_files_checkbox.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.move_files_checkbox = ctk.CTkCheckBox(self.options_frame, text="Move Files Based on Format", variable=self.move_files_var, font=ctk.CTkFont(size=14))
        self.move_files_checkbox.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.progress_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=14))
        self.progress_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20))

        self.process_button = ctk.CTkButton(self.main_frame, text="Process", command=self.process_files, font=ctk.CTkFont(size=14))
        self.process_button.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20))

    def process_files(self):
        directory = self.directory.get()
        self.progress_label.configure(text="Processing...")
        self.update()

        if self.delete_duplicates_var.get():
            self.delete_duplicates(directory)
        if self.move_files_var.get():
            self.organize_files(directory)
        if self.sort_files_var.get():
            self.sort_folders(directory)

        self.progress_label.configure(text="File organization completed.")

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

    def sort_folders(self, directory):
        folders = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        for folder in folders:
            size_mb = self.get_folder_size(folder)
            if size_mb <= 100:
                os.makedirs(os.path.join(directory, "small"), exist_ok=True)
                shutil.move(folder, os.path.join(directory, "small", os.path.basename(folder)))
            elif size_mb <= 500:
                os.makedirs(os.path.join(directory, "medium"), exist_ok=True)
                shutil.move(folder, os.path.join(directory, "medium", os.path.basename(folder)))
            elif size_mb <= 1000:
                os.makedirs(os.path.join(directory, "big"), exist_ok=True)
                shutil.move(folder, os.path.join(directory, "big", os.path.basename(folder)))

    def organize_files(self, directory):
        file_types = {
            "pdf files": (".pdf",),
            "image files": (".jpeg", ".jpg", ".png", ".PNG"),
            "archive files": (".zip", ".rar", ".7z"),
            "PPTX files": (".pptx",),
            "ipynb": (".ipynb",),
            "python": (".py",),
            "Excel files": (".xlsx", ".csv", ".xls"),
            "Exe": (".exe",),
            "Word Files": (".docx",),
            "Java": (".java",),
            "Text Files": (".txt",),
            "HTML files": (".html", ".htm"),
            "CSS files": (".css",),
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
            "Markdown files": (".md",),
            "JSON files": (".json",)
        }

        for file_type, extensions in file_types.items():
            files = [file for file in os.listdir(directory) if file.endswith(extensions)]
            if files:
                destination_dir = os.path.join(directory, file_type)
                self.move_files(directory, destination_dir, extensions)

if __name__ == "__main__":
    app = PythonFileManager()
    app.mainloop()