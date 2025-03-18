import asyncio
import fnmatch
import os
from threading import Thread
import tkinter as tk
import ttkbootstrap as ttk
from .properties import *
from .backup_gui import BackupGUI
from logger import logger
from backup import createBackupOf
from runtime_data import rtd
from miscellaneous.events import *


def _getSchemasNames() -> list[str]:
    schemas = [p.split('.')[0] for p in os.listdir('configs/schemas') 
               if fnmatch.fnmatch(p, '*.yml') or fnmatch.fnmatch(p, '*.yaml')]
    return schemas


class MenuGUI(ttk.Window):
    '''main startup window'''
    def __init__(self):
        super().__init__()
        self.title(f'{'[DEBUG] ' if DEBUG else ''}{PLUGIN_NAME} v{VERSION}')
        self.geometry('300x300')
        self.columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", lambda: self.after(0, self.quit))

        # --- preload ---

        # --- widgets ---
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, pady=10)

        self.selectSchema_cb = ttk.Combobox(self.main_frame, values=_getSchemasNames())
        self.selectSchema_cb.current(0)
        self.label1 = ttk.Label(self.main_frame, text='Schema: ', justify='right')
        self.backup_but = ttk.Button(self.main_frame, text='Backup', command=self.on_backup_but)

        self.label1.grid(row=0, column=0)
        self.selectSchema_cb.grid(row=0, column=1, )
        self.backup_but.grid(row=1, columnspan=2, sticky='ew', pady=4)

    # --- button methods ---------------------------------------------------------------------
    def on_backup_but(self):
        logger.info('=== STARTING BACKUP THREAD ===')
        
        def _backupThreadWorker():
            async def _cancelHandler():
                while True:
                    if getEvent('cancel-process'):
                        logger.info('canceling process...')
                        
                        # NOTE: important to pop useless data from runtime
                        rtd.tryPop('service')
                        rtd.tryPop('schema')
                        clearEvents()

                        loop.stop()
                        return
                    await asyncio.sleep(EVENT_UPDATE_DELAY)

            def _main():
                createBackupOf(self.selectSchema_cb.get())
                pushEvent('cancel-process')

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(asyncio.gather(
                    _cancelHandler(), 
                    asyncio.to_thread(_main),
                    return_exceptions=False
                ))
            except RuntimeError: pass
            loop.close()
            logger.info('=== END BACKUP PROCESS ===')

        backupGUI = BackupGUI(self, self.selectSchema_cb.get())
        backupThread = Thread(target=_backupThreadWorker, daemon=True)
        rtd['backup-thread'] = backupThread

        backupThread.start()
        self.wait_window(backupGUI)

        rtd.pop('backup-thread')
