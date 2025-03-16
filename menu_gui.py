import tkinter as tk
import ttkbootstrap as ttk
from .properties import *


class MenuGUI(ttk.Window):
    '''main startup window'''
    def __init__(self):
        super().__init__()
        self.title(f'{'[DEBUG] ' if DEBUG else ''}{PLUGIN_NAME} v{VERSION}')
        self.geometry('400x300')
        self.columnconfigure(0, weight=1)

        # --- preload ---

        # --- widgets ---
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, pady=10)

        self.selectSchema_cb = ttk.Combobox(self.main_frame, values=['test1', 'test2', 'test3'])
        self.selectSchema_cb.current(0)
        self.label1 = ttk.Label(self.main_frame, text='Schema: ', justify='right')
        self.backup_but = ttk.Button(self.main_frame, text='Backup')

        self.label1.grid(row=0, column=0)
        self.selectSchema_cb.grid(row=0, column=1, )
        self.backup_but.grid(row=1, columnspan=2, sticky='ew', pady=4)
