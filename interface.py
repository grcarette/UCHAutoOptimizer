import tkinter as tk
from tkinter import filedialog
from file_parser import FileParser
from level_handler import LevelHander
import os

class AOInterface:
    def __init__(self):
        self.lh = LevelHander()
        self.default_dir = os.path.join('C:\\Users', os.getlogin(), 'Appdata','LocalLow', 'Clever Endeavour Games', 'Ultimate Chicken Horse', 'snapshots')
        self.root = tk.Tk()
        self.root.title("Auto Optimizer - File Selector")
        self.root.geometry("400x300")
        
        self.label = tk.Label(self.root, text="No file selected.", wraplength=380)
        self.label.pack(pady=10)
        
        self.button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.button.pack(pady=5)

        # Optimize button
        self.optimize_button = tk.Button(self.root, text="Optimize", command=self.optimize_level)
        self.optimize_button.pack(pady=5)

        # Offset entry fields
        offset_frame = tk.Frame(self.root)
        offset_frame.pack(pady=5)

        tk.Label(offset_frame, text="X Offset:").grid(row=0, column=0, padx=5)
        self.x_offset_entry = tk.Entry(offset_frame, width=5)
        self.x_offset_entry.grid(row=0, column=1, padx=5)

        tk.Label(offset_frame, text="Y Offset:").grid(row=0, column=2, padx=5)
        self.y_offset_entry = tk.Entry(offset_frame, width=5)
        self.y_offset_entry.grid(row=0, column=3, padx=5)

        # Move level button
        self.move_button = tk.Button(self.root, text="Move Level", command=self.move_level)
        self.move_button.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.default_dir,
            title="Select a SNAPSHOT file",
            filetypes=[("SNAPSHOT Files", "*.snapshot"), ("All files", "*.*")]
        )
        if file_path:
            display_path = file_path.replace(self.default_dir, '').lstrip(os.sep)
            self.label.config(text=f"Selected:\n{display_path}")
            self.file_data = self.lh.set_filepath(file_path)

    def optimize_level(self):
        self.lh.optimize_level()

    def move_level(self):
        try:
            x_offset = int(self.x_offset_entry.get())
            y_offset = int(self.y_offset_entry.get())
            self.lh.move_level(x_offset, y_offset)
        except ValueError:
            self.label.config(text="Error: Offsets must be integers.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AOInterface()
    app.run()