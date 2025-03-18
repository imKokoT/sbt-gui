import sys
import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from properties import EVENT_UPDATE_DELAY


class BackupGUI(ttk.Toplevel):
    '''this window will show if backup process starts. its shows backup progress'''
    def __init__(self, parent, schemaName:str):
        super().__init__(parent)
        from . import styles
        
        self.title(f'Creating backup of "{schemaName}"')
        self.geometry('300x160')
        self.attributes("-toolwindow", False)
        self.resizable(False, False)
        
        # --- widgets ---
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', length=280, 
                                        style='SBT.Horizontal.TProgressbar')
        self.progress['value'] = 50
        self.progress.pack(pady=10, padx=10)
        
        self.transient(parent)  # Attach to main window
        self.grab_set()  # Lock interaction with the main window


    def _eventHandler(self):
        '''receive all tool events'''

        self.after(EVENT_UPDATE_DELAY, self._eventHandler)
