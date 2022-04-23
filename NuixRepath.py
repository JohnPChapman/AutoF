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

# Date and time
@traced
def now():
    rightNow = datetime.now()
    timeNow = rightNow.strftime("%d-%m-%Y %H-%M-%S")
    return timeNow


@traced
def repath(event=None):
    @traced
    def exitNR():
        windowRepath.destroy()

    @traced
    def dirSelect():
        myPath = filedialog.askdirectory(title="Select operation folder")
        dirFolderText.config(state=NORMAL)
        dirFolderText.delete(0, END)
        dirFolderText.insert(0, myPath)
        dirFolderText.config(state=DISABLED)

    @traced
    def dirImageSelect():
        imagePath = filedialog.askdirectory(title="Select Image folder")
        altImageText.config(state=NORMAL)
        altImageText.delete(0, END)
        altImageText.insert(0, imagePath)
        altImageText.config(state=DISABLED)

    # converts path for Windows COMPLETE
    @traced
    def convertPath(path):
        return path.replace('/', '\\')

    @traced
    def altImageBox():
        if altImageButton["state"] == NORMAL:
            altImageText.config(state=NORMAL)
            altImageText.delete(0, END)
            altImageText.config(state=DISABLED)
            altImageButton["state"] = DISABLED
        else:
            altImageButton["state"] = NORMAL

    @traced
    def run():
        runButton.config(state=DISABLED)
        logger = logging.getLogger('NuixRe-path')
        logger.setLevel(logging.DEBUG)
        progress = Progressbar(windowRepath, orient=HORIZONTAL, length=220, mode='indeterminate')
        progress.place(x=90, y=100)
        allFiles = []
        nxml = []
        imagesFound = []
        myPath = dirFolderText.get()
        if myPath == '':
            messagebox.showerror('Error!',
                                 'Operation root not selected!')
            return
        # create file handler which logs even debug messages
        log = myPath + '\\Re-Path ' + now() + '.log'
        fh = logging.FileHandler(log)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        # stores all files in list
        progress.start()
        if altImageButton["state"] == NORMAL and altImageText.get() != "":
            for iRoot, directories, files in os.walk(altImageText.get(), topdown=False):
                windowRepath.update()
                for file in files:
                    windowRepath.update()
                    allFiles.append(convertPath(iRoot) + '\\' + file)
        elif altImageButton["state"] == NORMAL and altImageText.get() == "":
            messagebox.showinfo("ERROR", "Alt Image ticked but not folder selected")
            return
        else:
            for iRoot, directories, files in os.walk(myPath, topdown=False):
                windowRepath.update()
                for file in files:
                    windowRepath.update()
                    allFiles.append(convertPath(iRoot) + '\\' + file)

        # Finds all xml, these contain the evidence locations
        for iRoot, directories, files in os.walk(myPath, topdown=False):
            windowRepath.update()
            for name in files:
                windowRepath.update()
                if '.xml' in name[-4:] and 'Evidence' in iRoot:
                    nxml.append(convertPath(os.path.join(iRoot, name)))

        # Sanitises list to ensure only nuix evidence files exist
        count = 0
        for i in nxml:
            windowRepath.update()
            nLog = 'false'
            f = open(i, 'r')
            for line in f:
                windowRepath.update()
                if 'evidence xmlns="http://nuix.com/fbi/evidence"' in line:
                    nLog = 'true'
            if nLog == 'false':
                nxml.pop(count)
            count = count + 1

        for i in nxml:
            windowRepath.update()
            found = 'false'
            f = open(i, 'r')
            rootDir = os.path.dirname(i)
            shutil.copy(i, rootDir + '\\' + os.path.basename(i)[:-4] + ' OLD ' + now())
            for line in f:
                windowRepath.update()
                if 'file location' in line:
                    # REGEX that finds everything between "" in a string that contains the above 'file location'
                    pattern = '"(.*?)"'
                    file = re.search(pattern, line).group(1)
                    if os.path.isfile(file):
                        logger.info(file + ' Exists in correct location.')
                        found = 'true'
                    else:

                        for name in allFiles:
                            windowRepath.update()
                            if os.path.basename(file).endswith(os.path.basename(name)):
                                imagesFound.append(convertPath(name))
                                fileIn = open(i, 'rt')
                                data = fileIn.read()
                                data = data.replace(file, os.path.join(name))
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(i, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('evidence replaced in ' + i)
                                found = 'true'
            if found == 'false':
                logger.error('')
                logger.error(' Image for ' + i + ' NOT FOUND')
                logger.error('')

        logger.info('------------------------------------------')
        logger.info('Cases Found')
        logger.info('------------------------------------------')
        for i in nxml:
            logger.info(i)
        logger.info('------------------------------------------')
        logger.info('Images Found')
        logger.info('------------------------------------------')
        if len(imagesFound) == 0:
            logger.info('Images not searched for.')
        else:
            for i in imagesFound:
                logger.info(i)
        progress.stop()
        messagebox.showinfo("Complete", "Re-pathing complete.")
        subprocess.Popen(['notepad.exe', log])
        progress.destroy()
        runButton.config(state=NORMAL)
    # Main window
    windowRepath = Tk()
    windowRepath.title("Nuix RePath")
    windowRepath.geometry("400x135")
    windowRepath.iconbitmap('settings\\ax.ico')
    windowRepath.resizable(width=False, height=False)
    windowRepath.lift()
    windowRepath.attributes('-topmost', True)

    # Operation Selection
    dirFolderText = Entry(windowRepath, width=40, bg="white", state=DISABLED)
    dirFolderText.place(x=15, y=25)
    dirImagesButton = Button(windowRepath, text="Select Root Folder", command=dirSelect, state=tk.NORMAL)
    dirImagesButton.place(x=270, y=22)

    # Image Path selection

    altImageCheck = Checkbutton(windowRepath, text="Alternate Image Path",
                                  command=altImageBox)
    altImageCheck.place(x=12, y=0)
    altImageText = Entry(windowRepath, width=40, bg="white", state=DISABLED)
    altImageText.place(x=15, y=65)
    altImageButton = Button(windowRepath, text="Select Image Folder", command=dirImageSelect, state=DISABLED)
    altImageButton.place(x=270, y=62)

    # Run button
    runButton = Button(windowRepath, text='Run', fg="green", command=run)
    runButton.place(x=350, y=100)
    exitButton = Button(windowRepath, text="Exit", fg="red", command=exitNR)
    exitButton.place(x=25, y=100)
    windowRepath.mainloop()