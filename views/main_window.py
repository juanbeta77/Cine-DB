import tkinter as tk
from tkinter import ttk
from .login_view import LoginPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cine-DB")
        self.geometry("800x600")

        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    def get_current_frame(self):
        return self._frame
