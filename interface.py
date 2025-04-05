import tkinter as tk
from tkinter import filedialog
from file_parser import FileParser

import os

class AOInterface:
    def __init__(self, default_dir="C:/Users/YourUsername/Documents/YourFolder"):
        self.fr = FileParser()
        self.default_dir = os.path.join('C:\\Users', os.getlogin(), 'Appdata','LocalLow', 'Clever Endeavour Games', 'Ultimate Chicken Horse', 'snapshots')
        self.root = tk.Tk()
        self.root.title("Auto Optimizer - File Selector")
        self.root.geometry("400x200")
        
        self.label = tk.Label(self.root, text="No file selected.", wraplength=380)
        self.label.pack(pady=20)
        
        self.button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.default_dir,
            title="Select a SNAPSHOT file",
            filetypes=[("SNAPSHOT Files", "*.snapshot"), ("All files", "*.*")]
        )
        if file_path:
            self.label.config(text=f"Selected:\n{file_path}")
            self.file_data = self.fr.parse_file(file_path)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AOInterface()
    app.run()