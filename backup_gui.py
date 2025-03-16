import tkinter as tk
import ttkbootstrap as ttk

class BackupGUI(ttk.Toplevel):
    '''this window will show if backup process starts. its shows backup progress'''
    def __init__(self, parent, schemaName:str):
        super().__init__(parent)
        self.title(f'Creating backup of {schemaName}')
        self.geometry('300x300')

        self.transient(parent)  # Attach to main window
        self.grab_set()  # Lock interaction with the main window
