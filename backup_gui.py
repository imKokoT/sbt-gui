import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from miscellaneous.events import pushEvent, getEvent, tryPopEvent
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
        self.logs_st = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=590, height=200)
        self.currentLog_l = ttk.Label(self, justify='left', font=('Arial', 8, 'italic'))

        self.progress_bar.pack(pady=16, padx=10, fill='x')
        self.currentLog_l.pack(pady=1, padx=10, fill='x')
        self.logs_st.pack(pady=15, padx=5, expand=True)
        
        # --- other ---
        self.transient(parent)  # Attach to main window
        self.grab_set()  # Lock interaction with the main window
        self._eventHandler()


    def _eventHandler(self):
        '''receive all tool events'''
        logs = tryPopEvent('log-pushed')
        if logs:
            self.logs_st.configure(state='normal')
            self.logs_st.insert(tk.END, '\n'.join(logs))
            self.logs_st.insert(tk.END, '\n')
            self.logs_st.see(tk.END)
            self.logs_st.configure(state='disabled')

            self.currentLog_l.config(text=logs[-1])

        progress = getEvent('update-progress')
        if progress:
            self.progress_bar['value'] = progress

        self.after(int(EVENT_UPDATE_DELAY*1000), self._eventHandler)
