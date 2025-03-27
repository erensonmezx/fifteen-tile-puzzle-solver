# src/ui/game_interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from typing import List, Optional
import time

from ..puzzle.puzzle_state import PuzzleState
from ..puzzle.solver import PuzzleSolver
from ..image_processing.image_handler import ImageHandler

class GameInterface:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("15-Puzzle Game")
        
        self.image_handler = ImageHandler()
        self.current_state = None
        self.solution_steps = None
        self.current_step = 0
        
        self._setup_ui()

    def _setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill='x', pady=(0, 10))

        self.load_btn = tk.Button(self.button_frame, text="Load Image", command=self._load_image)
        self.load_btn.pack(side='left', padx=5)

        self.shuffle_btn = tk.Button(self.button_frame, text="Shuffle", command=self._shuffle_puzzle)
        self.shuffle_btn.pack(side='left', padx=5)

        self.solve_btn = tk.Button(self.button_frame, text="Solve", command=self._solve_puzzle)
        self.solve_btn.pack(side='left', padx=5)

        self.next_btn = tk.Button(self.button_frame, text="Next Move", command=self._next_move)
        self.next_btn.pack(side='left', padx=5)
        self.next_btn.config(state='disabled')

        self.canvas = tk.Canvas(self.main_frame, width=300, height=300)
        self.canvas.pack(expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set("Load an image to start")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=5)

    def _load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            if self.image_handler.load_image(file_path):
                self.image_handler.split_image()
                self.current_state = PuzzleState()
                self._update_display()
                self.status_var.set("Image loaded. Click 'Shuffle' to start")
            else:
                messagebox.showerror("Error", "Failed to load image")

    def _shuffle_puzzle(self):
        if self.image_handler.tiles:
            self.current_state = PuzzleState.create_random_state()
            self._update_display()
            self.solution_steps = None
            self.current_step = 0
            self.next_btn.config(state='disabled')
            self.status_var.set("Puzzle shuffled. Click 'Solve' to find solution")

    def _solve_puzzle(self):
        if self.current_state:
            solver = PuzzleSolver(self.current_state)
            start_time = time.time()
            self.solution_steps = solver.get_solution_states()
            elapsed_time = time.time() - start_time
            
            if self.solution_steps:
                self.current_step = 0
                self.next_btn.config(state='normal')
                self.status_var.set(f"Solution found in {elapsed_time:.2f} seconds! {len(self.solution_steps)-1} moves")
            else:
                messagebox.showerror("Error", "No solution found")

    def _next_move(self):
        if self.solution_steps and self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            self.current_state = self.solution_steps[self.current_step]
            self._update_display()
            
            if self.current_step == len(self.solution_steps) - 1:
                self.next_btn.config(state='disabled')
                self.status_var.set("Puzzle solved!")
            else:
                self.status_var.set(f"Move {self.current_step} of {len(self.solution_steps)-1}")

    def _update_display(self):
        if not self.current_state or not self.image_handler.tiles:
            return

        flat_state = [num for row in self.current_state.state for num in row]
        merged = self.image_handler.merge_tiles(flat_state)
        
        image = cv2.cvtColor(merged, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=photo)
        self.canvas.image = photo

    def run(self):
        self.root.mainloop()