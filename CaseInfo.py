import os
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import logging
import re
import subprocess
from autologging import logged, TRACE, traced
from tkinter.ttk import Progressbar
import threading

# Date and time
@traced
def now():
    rightNow = datetime.now()
    timeNow = rightNow.strftime("%d-%m-%Y %H-%M-%S")
    return timeNow


@traced
def caseInfo(event=None):
    @traced
    def exitNR():
        windowCaseInfo.destroy()

    @traced
    def dirSelect():
        myPath = filedialog.askdirectory(title="Select operation folder")
        dirFolderText.config(state=NORMAL)
        dirFolderText.delete(0, END)
        dirFolderText.insert(0, myPath)
        dirFolderText.config(state=DISABLED)

    # converts path for Windows COMPLETE
    @traced
    def convertPath(path):
        return path.replace('/', '\\')

    @traced
    def run():
        runButton.config(state=DISABLED)
        windowCaseInfo.update()
        logger = logging.getLogger('Case Info')
        logger.setLevel(logging.DEBUG)
        allFiles = []
        nxml = []
        xcfg = []
        myPath = dirFolderText.get()
        if myPath == '':
            messagebox.showerror('Error!',
                                 'Operation root not selected!')
            return
        log = myPath + '\\Case Information ' + now() + '.txt'
        fh = logging.FileHandler(log, encoding='cp1252')
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        progress = Progressbar(windowCaseInfo, orient=HORIZONTAL, length=250, mode='indeterminate')
        progress.place(x=15, y=55)
        # Finds all files
        progress.start()
        for iRoot, directories, files in os.walk(myPath, topdown=False):
            windowCaseInfo.update()
            for name in files:
                windowCaseInfo.update()
                allFiles.append(convertPath(os.path.join(iRoot, name)))
        # Filters out nuix and X-Ways cases
        for i in allFiles:
            windowCaseInfo.update()
            if i.endswith('fbi2') and 'evidence.fbi2' not in i:
                nxml.append(convertPath(i))
            elif i.endswith('.xfc'):
                xcfg.append(convertPath(i))

        logger.info('--------------------')
        logger.info('Nuix Cases')
        logger.info('--------------------')
        if len(nxml) == 0:
            logger.info(' 0 Nuix cases found')
            logger.info('--------------------')
            logger.info('')
        else:
            logger.info(str(len(nxml)) + ' Nuix cases found')
            logger.info('--------------------')
            logger.info('')
        for i in nxml:
            f = open( i, 'r', encoding='UTF-8')
            for line in f:
                windowCaseInfo.update()
                if 'name' in line and 'graphDatabaseSettings' not in line and 'version' not in line:
                    l = line
                    l = l.replace('<name>', '')
                    l = l.replace('</name>', '')
                    logger.info(i)
                    logger.info(l.strip())
                elif 'saved-by-product' in line:
                    l = line
                    l = l.replace('<saved-by-product name="Nuix" version="','')
                    l = l.replace('" />','')
                    logger.info(l.strip())
                    logger.info('')


        logger.info('--------------------')
        logger.info('X-Ways Cases')
        logger.info('--------------------')
        if len(xcfg) == 0:
            logger.info(' 0 X-Ways cases found')
            logger.info('--------------------')
            logger.info('')
        else:
            logger.info(str(len(xcfg)) + ' X-Ways cases found')
            logger.info('--------------------')
            logger.info('')
        for i in xcfg:
            windowCaseInfo.update()
            f = open( i, 'r', encoding='cp1252', errors='ignore')
            filetext = f.read()
            f.close()
            matches = re.findall("X-Ways Forensics [0-9]*\.[0-9]+ SR-\d", filetext)
            logger.info(i)
            logger.info(matches[0])
            logger.info('')
        progress.stop()
        messagebox.showinfo("Complete", "Case search complete.")
        subprocess.Popen(['notepad.exe', log])
        progress.destroy()
        runButton.config(state=NORMAL)
    # Main window
    windowCaseInfo = Tk()
    windowCaseInfo.title("Case Info")
    windowCaseInfo.geometry("400x135")
    windowCaseInfo.iconbitmap('settings\\ax.ico')
    windowCaseInfo.resizable(width=False, height=False)
    windowCaseInfo.lift()
    windowCaseInfo.attributes('-topmost', True)

    # Operation Selection
    dirFolderText = Entry(windowCaseInfo, width=40, bg="white", state=DISABLED)
    dirFolderText.place(x=15, y=25)
    dirImagesButton = Button(windowCaseInfo, text="Select Root Folder", command=dirSelect, state=tk.NORMAL)
    dirImagesButton.place(x=270, y=22)


    # Run button
    runButton = Button(windowCaseInfo, text='Run', fg="green", command=run)
    runButton.place(x=350, y=100)
    exitButton = Button(windowCaseInfo, text="Exit", fg="red", command=exitNR)
    exitButton.place(x=25, y=100)
    windowCaseInfo.mainloop()