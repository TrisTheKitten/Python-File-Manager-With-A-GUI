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
        self.geometry("400x200")
        self.resizable(False, False)

        self.directory = ctk.StringVar()

        ctk.CTkLabel(self, text="Input the Directory:").pack(pady=10)
        self.directory_entry = ctk.CTkEntry(self, textvariable=self.directory, width=300)
        self.directory_entry.pack(pady=5)

        self.progress_label = ctk.CTkLabel(self, text="")
        self.progress_label.pack(pady=10)

        ctk.CTkButton(self, text="Process", command=self.process_files).pack(pady=10)

    def process_files(self):
        directory = self.directory.get()
        self.progress_label.configure(text="Processing...")
        self.update()

        self.delete_duplicates(directory)
        self.organize_files(directory)
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