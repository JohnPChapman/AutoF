# Auto Imaging functions Version 0.1
from autologging import logged, TRACE, traced
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import sqlite3
import os
from AutoS import convertPath


@traced
def imageMonitor(tool, imagePath, casePath, profile):

    def end():
        progress.stop()
        imagesWindow.destroy()
        messagebox.showinfo("Complete", "Process complete.")

    def scan():
        print('hello')

        def getAttributes():
            sconn = sqlite3.connect('settings\\settings.db ')
            scur = sconn.cursor()
            scur.execute("Select * FROM Settings")
            sconn.commit()
            rows = scur.fetchall()

            optionsDriveLogSettingsText = rows[0][1]
            optionsImageCompleteText = rows[0][2]
            optionsImageIntegrityText = rows[0][3]

            return optionsDriveLogSettingsText, optionsImageCompleteText, optionsImageIntegrityText

        found = []
        isLog = []
        isReady = []
        file, complete, integrity = getAttributes()
        file = file.split(',')
        for i in file:
            for iRoot, directories, files in os.walk(str(imagePath), topdown=False):
                for name in files:
                    if name.endswith(i):
                        found.append(convertPath(os.path.join(iRoot, name)))
            for r in found:
                with open(r) as log:
                    lines = log.readlines()
                for l in lines:
                    if complete in l:
                        isLog.append(r)

        if integrity != '':
            for i in isLog:
                with open(i) as log:
                    lines = log.readlines()
                    for l in lines:
                        if integrity in l:
                            isReady.append(os.path.dirname(i) + '\\')
        print(isReady)
        # time.sleep(30)

    imagesWindow = Tk()
    imagesWindow.title("AutoF Image Monitor")
    imagesWindow.geometry("400x200")
    imagesWindow.resizable(width=False, height=False)
    exitButton = Button(imagesWindow, text="Exit", fg="red", command=end)
    exitButton.place(x=20, y=160)

    testButton = Button(imagesWindow, text="Test", fg="red", command=scan)
    testButton.place(x=350, y=160)
    progress = Progressbar(imagesWindow, orient=HORIZONTAL, length=250, mode='indeterminate')
    progress.place(x=70, y=30)
    progress.start(20)
