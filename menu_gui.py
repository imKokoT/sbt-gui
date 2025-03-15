import tkinter as tk
import ttkbootstrap as ttk
from .properties import *


class MenuGUI(ttk.Window):
    '''main startup window'''
    def __init__(self):
        super().__init__()
        self.title(f'{PLUGIN_NAME} v{VERSION}')
        self.geometry('400x300')

        self.label = ttk.Label(self, text="Hello, ttkbootstrap!", font=("Arial", 14))
        self.button = ttk.Button(self, text="Click Me",  command=self.onButClick)

        self.label.pack(pady=20)
        self.button.pack(pady=10)

    def onButClick(self):
        self.label.config(text="Button Clicked!")
