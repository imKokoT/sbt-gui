import sys
import threading
import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from miscellaneous.events import pushEvent
from properties import EVENT_UPDATE_DELAY


class BackupGUI(ttk.Toplevel):
    '''this window will show if backup process starts. its shows backup progress'''
    def __init__(self, parent, schemaName:str):
        super().__init__(parent)
        from . import styles
        
        self.title(f'Creating backup of "{schemaName}"')
        self.geometry('600x300')
        self.attributes("-toolwindow", False)
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: (pushEvent('cancel-process'), self.after(0, self.destroy))[-1])
        
        # --- widgets ---
        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', length=580, maximum=1,
                                        style='SBT.Horizontal.TProgressbar')
        self.progress_bar['value'] = 0.5
        self.logs_st = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=590, height=200)

        self.progress_bar.pack(pady=10, padx=10, fill='x')
        self.logs_st.pack(pady=15, padx=5, expand=True)
        
        # --- other ---
        self.transient(parent)  # Attach to main window
        self.grab_set()  # Lock interaction with the main window


    def _eventHandler(self):
        '''receive all tool events'''

        self.after(EVENT_UPDATE_DELAY, self._eventHandler)
